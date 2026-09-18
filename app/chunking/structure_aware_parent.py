from datetime import datetime
from typing import List, Optional

from app.config.settings import ChunkingConfig
from app.models.document import Document
from app.models.elements import StructuralElement
from app.models.metadata import (
    ChunkMetadata,
    ContentType,
    HeadingContext,
)
from app.models.parent_chunk import ParentChunk

# ============================================================
# STRUCTURE-AWARE PARENT CHUNKER
# ============================================================


class StructureAwareParentChunker:
    """
    Converts structure-aware document elements into ParentChunk objects.

    Responsibilities
    ----------------
    1. Preserve document structure and heading context.
    2. Group paragraphs/text into logical parent chunks.
    3. Treat code blocks as strong boundaries.
    4. Respect the configured maximum parent chunk size.
    5. Generate production metadata.
    6. Generate stable content hashes for parent content.

    This class is responsible ONLY for parent generation.

    It does not:
        - create child chunks
        - generate embeddings
        - store data in MongoDB
        - store data in Qdrant
    """

    def __init__(
        self,
        config: ChunkingConfig,
    ) -> None:

        self.config = config

    # ========================================================
    # PUBLIC API
    # ========================================================

    def chunk(
        self,
        document: Document,
        elements: List[StructuralElement],
    ) -> List[ParentChunk]:
        """
        Convert structural elements into parent chunks.

        Parameters
        ----------
        document:
            Source document.

        elements:
            Structure-aware elements extracted from the document.

        Returns
        -------
        List[ParentChunk]
            Generated parent chunks.
        """

        parents: List[ParentChunk] = []

        buffer: List[str] = []
        buffer_types: List[str] = []

        current_context: Optional[HeadingContext] = None

        parent_index = 0

        # ----------------------------------------------------
        # Local flush function
        # ----------------------------------------------------

        def create_parent() -> None:
            nonlocal parent_index

            if not buffer:
                return

            content = "\n\n".join(buffer).strip()

            if not content:
                return

            # Pydantic v2:
            # use model_copy() instead of copy().
            context = (
                current_context.model_copy(deep=True)
                if current_context is not None
                else HeadingContext()
            )

            content_type = self._primary_content_type(buffer_types)

            content_hash = ParentChunk.create_content_hash(content)

            parent_key = ParentChunk.create_parent_key(
                document_id=document.document_id,
                parent_index=parent_index,
                section_path=context.get_section_path(),
                content_hash=content_hash,
            )

            metadata = self._build_metadata(
                content=content,
                content_type=content_type,
                source=document.source,
            )

            parent = ParentChunk(
                parent_index=parent_index,
                parent_key=parent_key,
                document_id=document.document_id,
                content=content,
                content_type=content_type,
                source=document.source,
                heading_context=context,
                metadata=metadata,
                content_hash=content_hash,
            )

            parents.append(parent)

            parent_index += 1

            buffer.clear()
            buffer_types.clear()

        # ====================================================
        # PROCESS STRUCTURAL ELEMENTS
        # ====================================================

        for element in elements:

            # ------------------------------------------------
            # HEADING
            # ------------------------------------------------

            if element.element_type == "heading":

                # A heading starts a new logical section.
                #
                # Therefore:
                #
                # 1. Flush content belonging to the
                #    previous section.
                #
                # 2. Update heading context.
                #
                # 3. Continue processing subsequent content.

                create_parent()

                current_context = element.heading_context.model_copy(deep=True)

                continue

            # ------------------------------------------------
            # CODE
            # ------------------------------------------------

            if element.element_type == "code":

                # Code is treated as a strong logical boundary.
                #
                # Flush whatever came before the code first.

                create_parent()

                current_context = element.heading_context.model_copy(deep=True)

                content = element.content.strip()

                if not content:
                    continue

                buffer.append(content)
                buffer_types.append("code")

                # Code becomes its own parent chunk.

                create_parent()

                continue

            # ------------------------------------------------
            # LIST
            # ------------------------------------------------

            if element.element_type == "list":

                current_context = element.heading_context.model_copy(deep=True)

                content = element.content.strip()

                if not content:
                    continue

                current_length = self._buffer_length(buffer)

                if (
                    buffer
                    and current_length + len(content) > self.config.max_chunk_chars
                ):
                    create_parent()

                buffer.append(content)
                buffer_types.append("list")

                continue

            # ------------------------------------------------
            # PARAGRAPH / TEXT
            # ------------------------------------------------

            if element.element_type in {"paragraph", "text"}:

                content = element.content.strip()

                if not content:
                    continue

                current_context = element.heading_context.model_copy(deep=True)

                current_length = self._buffer_length(buffer)

                if (
                    buffer
                    and current_length + len(content) > self.config.max_chunk_chars
                ):
                    create_parent()

                buffer.append(content)
                buffer_types.append(element.element_type)

                continue

        # ====================================================
        # FINAL PARENT
        # ====================================================

        create_parent()

        return parents

    # ========================================================
    # BUFFER HELPERS
    # ========================================================

    @staticmethod
    def _buffer_length(
        buffer: List[str],
    ) -> int:
        """
        Return the character length of the current buffer.

        Paragraphs/elements are joined using two newline
        characters, matching the final parent content format.
        """

        return len("\n\n".join(buffer))

    # ========================================================
    # CONTENT TYPE
    # ========================================================

    @staticmethod
    def _primary_content_type(
        buffer_types: List[str],
    ) -> ContentType:
        """
        Determine the logical content type of a parent.

        Priority:
            1. code
            2. list-only
            3. mixed/paragraph content
        """

        if not buffer_types:
            return ContentType.TEXT

        # Code is treated as the dominant logical type.
        if "code" in buffer_types:
            return ContentType.CODE

        # A parent containing only list content
        # is classified as LIST.
        if (
            "list" in buffer_types
            and "paragraph" not in buffer_types
            and "text" not in buffer_types
        ):
            return ContentType.LIST

        # Paragraph + list or paragraph + other content
        # represents a mixed structural parent.
        if "paragraph" in buffer_types or "text" in buffer_types:
            return ContentType.MIXED

        return ContentType.MIXED

    # ========================================================
    # SOURCE TYPE
    # ========================================================

    @staticmethod
    def _detect_source_type(
        source: str,
    ) -> str:
        """
        Detect the source type from the source name/path.

        This is deliberately separate from ContentType.

        Example:
            source_type = "pdf"
            content_type = ContentType.TEXT
        """

        normalized_source = source.lower()

        if normalized_source.endswith(".md"):
            return "markdown"

        if normalized_source.endswith(".pdf"):
            return "pdf"

        if normalized_source.endswith(".html"):
            return "html"

        if normalized_source.endswith(".htm"):
            return "html"

        if normalized_source.endswith(".docx"):
            return "docx"

        if normalized_source.endswith(".txt"):
            return "text"

        return "unknown"

    # ========================================================
    # METADATA
    # ========================================================

    def _build_metadata(
        self,
        content: str,
        content_type: ContentType,
        source: str,
    ) -> ChunkMetadata:

        return ChunkMetadata(
            source_type=self._detect_source_type(source),
            ingestion_version=(self.config.ingestion_version),
            char_count=len(content),
            chunking_strategy=("structure_aware_parent"),
            chunking_version=(self.config.parent_chunking_version),
            language="en",
            content_type=content_type,
            ingestion_timestamp=datetime.now(),
        )

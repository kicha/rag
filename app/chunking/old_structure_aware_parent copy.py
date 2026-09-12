from typing import List, Optional
from datetime import datetime
import uuid

from app.models.document import Document
from app.models.parent_chunk import ParentChunk
from app.config.settings import ChunkingConfig
from app.models.elements import StructuralElement
from app.models.metadata import HeadingContext, ChunkMetadata, ContentType

# ============================================================
# STRUCTURE-AWARE CHUNKER V3
# ============================================================


class StructureAwareChunker:

    def __init__(
        self,
        config: ChunkingConfig,
    ):

        self.config = config

    def chunk(
        self,
        document: Document,
        elements: List[StructuralElement],
    ) -> List[ParentChunk]:

        parents: List[ParentChunk] = []

        buffer: List[str] = []

        buffer_types: List[str] = []

        current_context: Optional[HeadingContext] = None

        parent_index = 0

        # ----------------------------------------------------
        # Helper functions
        # ----------------------------------------------------

        def buffer_length() -> int:

            return len("\n\n".join(buffer))

        def primary_content_type() -> ContentType:

            if not buffer_types:
                return ContentType.TEXT

            # If there is code, code is the
            # dominant logical type.
            if "code" in buffer_types:

                return ContentType.CODE

            # If list exists and there is
            # no normal paragraph, classify
            # as list.
            if "list" in buffer_types and "paragraph" not in buffer_types:

                return ContentType.LIST

            # Heading + paragraph/list is a
            # section-level chunk.
            if "paragraph" in buffer_types:

                return ContentType.MIXED

            return ContentType.MIXED

        def create_chunk():

            nonlocal parent_index

            if not buffer:

                return

            content = "\n\n".join(buffer).strip()

            if not content:

                return

            context = current_context.copy() if current_context else HeadingContext()

            content_type = primary_content_type()

            # ------------------------------------------------
            # Production metadata
            # ------------------------------------------------

            metadata = ChunkMetadata(
                h1=context.h1,
                h2=context.h2,
                h3=context.h3,
                h4=context.h4,
                h5=context.h5,
                h6=context.h6,
                section_path=context.get_section_path(),
                char_count=len(content),
                chunking_strategy="structure_aware",
                chunking_version="structure_aware_v3",
                source_type="markdown",
                language="en",
                content_type=content_type,
                ingestion_timestamp=datetime.now(),
            )

            # ------------------------------------------------
            # Create Pydantic Chunk
            # ------------------------------------------------

            parent_chunk = ParentChunk(
                parent_id=str(uuid.uuid4()),
                parent_index=parent_index,
                document_id=(document.document_id),
                content=content,
                content_type=content_type,
                content_hash=ParentChunk.create_content_hash(content),
                source=document.source,
                heading_context=context,
                metadata=metadata,
            )

            parents.append(parent_chunk)

            parent_index += 1

            buffer.clear()
            buffer_types.clear()

        # ----------------------------------------------------
        # Process structural elements
        # ----------------------------------------------------

        for element in elements:

            # ------------------------------------------------
            # HEADING
            # ------------------------------------------------

            if element.element_type == "heading":

                # A heading marks a logical section boundary.
                #
                # Therefore, finalize whatever content
                # belongs to the previous section BEFORE
                # changing the heading context.

                create_chunk()

                # Now update the context for the
                # content that follows this heading.
                current_context = element.heading_context.copy()

                continue

            # ------------------------------------------------
            # CODE
            # ------------------------------------------------

            if element.element_type == "code":

                # A code block is a strong
                # logical boundary.

                create_chunk()

                current_context = element.heading_context.copy()

                buffer.append(element.content.strip())

                buffer_types.append("code")

                create_chunk()

                continue

            # ------------------------------------------------
            # LIST
            # ------------------------------------------------

            if element.element_type == "list":

                current_context = element.heading_context.copy()
                content = element.content.strip()

                if not content:
                    continue

                current_length = buffer_length()

                if (
                    buffer
                    and current_length + len(content) > self.config.max_chunk_chars
                ):

                    create_chunk()

                buffer.append(content)

                buffer_types.append("list")

                continue

            # ------------------------------------------------
            # PARAGRAPH
            # ------------------------------------------------

            if element.element_type in {"paragraph", "text"}:

                content = element.content.strip()
                if not content:
                    continue
                current_length = buffer_length()

                # If the current section already contains content
                # and adding this element would exceed the size limit,
                # finalize the current chunk first.
                if (
                    buffer
                    and current_length + len(content) > self.config.max_chunk_chars
                ):
                    create_chunk()

                buffer.append(content)
                buffer_types.append(element.element_type)
        # ----------------------------------------------------
        # Final chunk
        # ----------------------------------------------------

        create_chunk()

        return parents

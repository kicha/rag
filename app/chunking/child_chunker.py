from typing import List

from app.config.settings import ChunkingConfig
from app.models.child_chunk import ChildChunk
from app.models.metadata import ChunkMetadata
from app.models.parent_chunk import ParentChunk

# ============================================================
# CHILD CHUNKER
# ============================================================


class ChildChunker:
    """
    Splits persisted ParentChunk objects into smaller
    retrievable ChildChunk objects.

    Responsibilities
    ----------------
    1. Split parent content into smaller child chunks.
    2. Apply configurable child overlap.
    3. Preserve document and structural metadata.
    4. Preserve the persisted parent_id relationship.
    5. Generate child content hashes.

    This class does NOT:
        - generate embeddings
        - write to Qdrant
        - write to MongoDB
        - retrieve parent chunks
    """

    def __init__(
        self,
        config: ChunkingConfig,
    ) -> None:

        self.config = config

        self._validate_config()

    # ========================================================
    # PUBLIC API
    # ========================================================

    def chunk_parent(
        self,
        parent: ParentChunk,
    ) -> List[ChildChunk]:
        """
        Split one ParentChunk into ChildChunk objects.

        child_index is local to the parent:

            parent A
                child_index=0
                child_index=1

            parent B
                child_index=0
                child_index=1
        """

        child_contents = self._split_content(parent.content)

        children: List[ChildChunk] = []

        for child_index, content in enumerate(child_contents):

            metadata = self._build_metadata(
                parent=parent,
                content=content,
            )

            child = ChildChunk(
                document_id=parent.document_id,
                content=content,
                content_type=parent.content_type,
                source=parent.source,
                heading_context=(parent.heading_context.model_copy(deep=True)),
                metadata=metadata,
                content_hash=(ChildChunk.create_content_hash(content)),
                parent_id=parent.parent_id,
                child_index=child_index,
            )

            children.append(child)

        return children

    # ========================================================
    # CHUNK MULTIPLE PARENTS
    # ========================================================

    def chunk_parents(
        self,
        parents: List[ParentChunk],
    ) -> List[ChildChunk]:
        """
        Split multiple ParentChunk objects into children.
        """

        children: List[ChildChunk] = []

        for parent in parents:

            parent_children = self.chunk_parent(parent)

            children.extend(parent_children)

        return children

    # ========================================================
    # CONTENT SPLITTING
    # ========================================================

    def _split_content(
        self,
        content: str,
    ) -> List[str]:
        """
        Split text using a maximum character window while
        preferring whitespace boundaries.

        The next child begins with configurable overlap from
        the previous child.

        This is deliberately implemented without LangChain so
        that chunking behavior remains visible and testable.
        """

        content = content.strip()

        if not content:
            return []

        child_size = self.config.child_chunk_chars

        overlap = self.config.child_overlap_chars

        # ----------------------------------------------------
        # Parent already fits inside one child.
        # ----------------------------------------------------

        if len(content) <= child_size:
            return [content]

        chunks: List[str] = []

        start = 0
        content_length = len(content)

        while start < content_length:

            # ------------------------------------------------
            # Maximum possible end for this child.
            # ------------------------------------------------

            max_end = min(
                start + child_size,
                content_length,
            )

            # ------------------------------------------------
            # Last child.
            # ------------------------------------------------

            if max_end == content_length:

                end = content_length

            else:

                # --------------------------------------------
                # Prefer a whitespace boundary rather than
                # cutting through a word.
                # --------------------------------------------

                candidate = content[start:max_end]

                boundary = candidate.rfind(" ")

                # --------------------------------------------
                # Do not accept an extremely early boundary.
                #
                # Example:
                #
                # child_size = 120
                #
                # We do not want a chunk of 20 chars merely
                # because whitespace happened there.
                # --------------------------------------------

                minimum_boundary = int(child_size * 0.60)

                if boundary >= minimum_boundary:

                    end = start + boundary

                else:

                    end = max_end

            # ------------------------------------------------
            # Extract child.
            # ------------------------------------------------

            child_content = content[start:end].strip()

            if child_content:

                chunks.append(child_content)

            # ------------------------------------------------
            # Finished.
            # ------------------------------------------------

            if end >= content_length:
                break

            # ------------------------------------------------
            # Apply overlap.
            # ------------------------------------------------

            next_start = max(
                0,
                end - overlap,
            )

            # ------------------------------------------------
            # Avoid starting halfway through a word.
            # Move forward until whitespace boundary.
            # ------------------------------------------------

            while (
                next_start < end
                and next_start > 0
                and not content[next_start - 1].isspace()
            ):

                next_start += 1

            # ------------------------------------------------
            # Defensive protection against infinite loops.
            # ------------------------------------------------

            if next_start <= start:

                next_start = end

            start = next_start

        return chunks

    # ========================================================
    # CHILD METADATA
    # ========================================================

    @staticmethod
    def _build_metadata(
        parent: ParentChunk,
        content: str,
    ) -> ChunkMetadata:
        """
        Child metadata begins as a deep copy of parent
        metadata.

        We then modify fields whose meaning differs for the
        child.
        """

        metadata = parent.metadata.model_copy(deep=True)

        metadata.char_count = len(content)

        metadata.chunking_strategy = "parent_child"

        metadata.chunking_version = "1.0"

        metadata.parent_chunk_id = parent.parent_id

        return metadata

    # ========================================================
    # CONFIG VALIDATION
    # ========================================================

    def _validate_config(
        self,
    ) -> None:

        if self.config.child_chunk_chars <= 0:

            raise ValueError("child_chunk_chars must be greater " "than zero.")

        if self.config.child_overlap_chars < 0:

            raise ValueError("child_overlap_chars cannot be " "negative.")

        if self.config.child_overlap_chars >= self.config.child_chunk_chars:

            raise ValueError(
                "child_overlap_chars must be smaller " "than child_chunk_chars."
            )

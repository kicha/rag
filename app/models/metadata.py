from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

from pydantic import BaseModel

from app.models.document import Document

# ============================================================
# CONTENT TYPE
# ============================================================


class ContentType(str, Enum):

    TEXT = "text"
    CODE = "code"
    LIST = "list"
    TABLE = "table"
    IMAGE = "image"
    MIXED = "mixed"


# ============================================================
# HEADING CONTEXT
# ============================================================


class HeadingContext(BaseModel):

    h1: Optional[str] = None
    h2: Optional[str] = None
    h3: Optional[str] = None
    h4: Optional[str] = None
    h5: Optional[str] = None
    h6: Optional[str] = None

    def update(
        self,
        level: int,
        heading: str,
    ) -> None:

        if level < 1 or level > 6:
            raise ValueError("Heading level must be between 1 and 6.")

        setattr(
            self,
            f"h{level}",
            heading,
        )

        # Clear lower-level headings because a new heading
        # closes the previous lower hierarchy.
        for lower_level in range(
            level + 1,
            7,
        ):
            setattr(
                self,
                f"h{lower_level}",
                None,
            )

    def get_section_path(self) -> List[str]:

        return [
            value
            for level in range(1, 7)
            if (
                value := getattr(
                    self,
                    f"h{level}",
                )
            )
        ]

    def clone(self) -> "HeadingContext":

        return self.model_copy(
            deep=True,
        )

    def as_dict(self) -> Dict[str, Optional[str]]:

        return {
            "h1": self.h1,
            "h2": self.h2,
            "h3": self.h3,
            "h4": self.h4,
            "h5": self.h5,
            "h6": self.h6,
        }


# ============================================================
# CHUNK METADATA
# ============================================================


class ChunkMetadata(BaseModel):
    """
    Operational metadata belonging to a chunk.

    IMPORTANT:
    Heading hierarchy does NOT live here.

    HeadingContext is the canonical source for:
        h1 ... h6
        section_path

    This prevents structural metadata from being duplicated
    in MongoDB and Qdrant domain models.
    """

    # --------------------------------------------------------
    # SOURCE / INGESTION
    # --------------------------------------------------------

    source_type: str = "markdown"

    ingestion_version: str = "benchmark_v2"

    ingestion_timestamp: Optional[datetime] = None

    # --------------------------------------------------------
    # CONTENT CHARACTERISTICS
    # --------------------------------------------------------

    char_count: int = 0

    token_count: Optional[int] = None

    # --------------------------------------------------------
    # CHUNKING
    # --------------------------------------------------------

    chunking_strategy: str = "structure_aware"

    chunking_version: str = "1.0"

    # --------------------------------------------------------
    # DOCUMENT LOCATION
    # --------------------------------------------------------

    page_number: Optional[int] = None

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language: str = "en"

    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    content_type: str

    # --------------------------------------------------------
    # RELATIONSHIP
    # --------------------------------------------------------

    parent_chunk_id: Optional[str] = None

    # --------------------------------------------------------
    # PAYLOAD SERIALIZATION
    # --------------------------------------------------------

    def to_payload(self) -> dict:

        return self.model_dump(
            mode="json",
        )


# ============================================================
# METADATA ENRICHER
# ============================================================


class MetadataEnricher:

    def __init__(
        self,
        document: Document,
        ingestion_version: str = "benchmark_v2",
    ):
        self.document = document
        self.ingestion_version = ingestion_version

    def enrich(
        self,
        text: str,
        heading_context: HeadingContext,
        content_type: str,
        chunk_index: int,
    ) -> ChunkMetadata:

        # heading_context and chunk_index are intentionally
        # accepted because callers work at structural level,
        # but hierarchy itself is stored on BaseChunk.

        return ChunkMetadata(
            source_type=self._detect_source_type(),
            ingestion_version=self.ingestion_version,
            content_type=content_type,
            char_count=len(text),
        )

    def _detect_source_type(self) -> str:

        source = self.document.source.lower()

        if source.endswith(".pdf"):
            return "pdf"

        if source.endswith(".md"):
            return "markdown"

        if source.endswith(".html"):
            return "html"

        if source.endswith(".htm"):
            return "html"

        if source.endswith(".txt"):
            return "text"

        if source.endswith(".docx"):
            return "docx"

        return "unknown"

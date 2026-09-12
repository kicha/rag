from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

from app.models.document import Document
from app.utils.hashing import ChunkIdGenerator


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

        setattr(
            self,
            f"h{level}",
            heading,
        )

        # Clear lower levels.
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

        path = []

        for level in range(1, 7):

            value = getattr(
                self,
                f"h{level}",
            )

            if value:
                path.append(value)

        return path

    def clone(self) -> "HeadingContext":

        return HeadingContext(
            h1=self.h1,
            h2=self.h2,
            h3=self.h3,
            h4=self.h4,
            h5=self.h5,
            h6=self.h6,
        )

    def as_dict(self) -> Dict:

        return {
            "h1": self.h1,
            "h2": self.h2,
            "h3": self.h3,
            "h4": self.h4,
            "h5": self.h5,
            "h6": self.h6,
        }


# ============================================================
# CHUNK META DATA
# ============================================================


class ChunkMetadata(BaseModel):

    # =========================================================
    # SOURCE / INGESTION
    # =========================================================

    source_type: str = "markdown"

    ingestion_version: str = "v1"

    ingestion_timestamp: Optional[datetime] = None

    # =========================================================
    # DOCUMENT STRUCTURE
    # =========================================================

    h1: Optional[str] = None
    h2: Optional[str] = None
    h3: Optional[str] = None
    h4: Optional[str] = None
    h5: Optional[str] = None
    h6: Optional[str] = None

    section_path: list[str] = Field(default_factory=list)

    # =========================================================
    # CONTENT CHARACTERISTICS
    # =========================================================

    char_count: int = 0

    token_count: Optional[int] = None

    # =========================================================
    # CHUNKING
    # =========================================================

    chunking_strategy: str = "structure_aware"

    chunking_version: str = "structure_aware_v3"

    # =========================================================
    # DOCUMENT LOCATION
    # =========================================================

    page_number: Optional[int] = None

    # =========================================================
    # LANGUAGE
    # =========================================================

    language: str = "en"

    # =========================================================
    # CONTENT FLAGS
    # =========================================================

    content_type: str

    # =========================================================
    # PARENT / CHILD RETRIEVAL
    # =========================================================

    parent_chunk_id: Optional[str] = None

    # =========================================================
    # QDRANT PAYLOAD
    # =========================================================

    def to_payload(self) -> dict:
        """
        Convert metadata into a JSON-compatible
        Qdrant payload fragment.
        """

        return self.model_dump(mode="json")


class MetadataEnricher:

    def __init__(
        self,
        document: Document,
        ingestion_version: str = "1.0",
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

        chunk_id = ChunkIdGenerator.generate(
            document_id=self.document.document_id,
            chunk_index=chunk_index,
        )

        section_path = heading_context.get_section_path()

        return ChunkMetadata(
            source_type=self._detect_source_type(),
            ingestion_version=self.ingestion_version,
            h1=heading_context.h1,
            h2=heading_context.h2,
            h3=heading_context.h3,
            h4=heading_context.h4,
            h5=heading_context.h5,
            h6=heading_context.h6,
            section_path=section_path,
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

        if source.endswith(".txt"):
            return "text"

        return "unknown"

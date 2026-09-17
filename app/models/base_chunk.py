from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field

from app.models.metadata import (
    ChunkMetadata,
    ContentType,
    HeadingContext,
)

from app.utils.hashing import (
    generate_content_hash,
)


class BaseChunk(BaseModel):
    document_id: str
    content: str
    content_type: ContentType
    source: str

    # Canonical structural hierarchy.
    heading_context: HeadingContext

    # Operational metadata.
    metadata: ChunkMetadata
    content_hash: str
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ========================================================
    # DERIVED PROPERTIES
    # ========================================================

    @property
    def char_count(self) -> int:

        return len(self.content)

    @property
    def section_path(self) -> List[str]:

        return self.heading_context.get_section_path()

    # ========================================================
    # CONTENT HASH
    # ========================================================

    @classmethod
    def create_content_hash(
        cls,
        content: str,
    ) -> str:

        return generate_content_hash(content)

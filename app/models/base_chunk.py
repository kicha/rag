from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List
from app.models.metadata import ChunkMetadata, ContentType, HeadingContext
from app.utils.hashing import generate_content_hash

# ============================================================
# CHUNK
# ============================================================


class BaseChunk(BaseModel):
    document_id: str
    content: str
    content_type: ContentType
    source: str
    heading_context: HeadingContext
    metadata: ChunkMetadata
    content_hash: str
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def char_count(self) -> int:
        return len(self.content)

    @classmethod
    def create_content_hash(
        cls,
        content: str,
    ) -> str:
        return generate_content_hash(content)

    @property
    def section_path(self) -> List[str]:
        return self.heading_context.get_section_path()

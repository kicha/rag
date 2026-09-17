from datetime import datetime, timezone
from uuid import uuid4

from pydantic import Field

from app.models.base_chunk import BaseChunk
from app.utils.hashing import ChunkKeyGenerator


class ParentChunk(BaseChunk):

    # Runtime identity.
    parent_id: str = Field(default_factory=lambda: str(uuid4()))
    parent_index: int

    # Stable benchmark/evaluation identity.
    parent_key: str

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ========================================================
    # KEY FACTORY
    # ========================================================

    @staticmethod
    def create_parent_key(
        document_id: str,
        parent_index: int,
        section_path: list[str],
        content_hash: str,
    ) -> str:

        return ChunkKeyGenerator.generate_parent_key(
            document_id=document_id,
            parent_index=parent_index,
            section_path=section_path,
            content_hash=content_hash,
        )

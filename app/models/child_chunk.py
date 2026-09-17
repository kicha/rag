from uuid import uuid4

from pydantic import Field

from app.models.base_chunk import BaseChunk
from app.utils.hashing import ChunkKeyGenerator


class ChildChunk(BaseChunk):

    # Runtime Qdrant point identity.
    child_id: str = Field(default_factory=lambda: str(uuid4()))

    # Runtime relation back to MongoDB.
    parent_id: str

    # Stable relation for benchmark/evaluation.
    parent_key: str

    child_index: int

    # Stable benchmark/evaluation identity.
    child_key: str

    # ========================================================
    # KEY FACTORY
    # ========================================================

    @staticmethod
    def create_child_key(
        parent_key: str,
        child_index: int,
        content_hash: str,
    ) -> str:

        return ChunkKeyGenerator.generate_child_key(
            parent_key=parent_key,
            child_index=child_index,
            content_hash=content_hash,
        )

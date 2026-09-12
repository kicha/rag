from pydantic import Field
from uuid import uuid4

from app.models.base_chunk import BaseChunk

# ============================================================
# CHUNK
# ============================================================


class ChildChunk(BaseChunk):

    child_id: str = Field(default_factory=lambda: str(uuid4()))
    parent_id: str
    child_index: int

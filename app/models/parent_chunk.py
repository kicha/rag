from datetime import datetime, timezone
from uuid import uuid4
from pydantic import Field
from app.models.base_chunk import BaseChunk

# ============================================================
# PARENT CHUNK
# ============================================================


class ParentChunk(BaseChunk):

    parent_id: str = Field(default_factory=lambda: str(uuid4()))
    parent_index: int
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

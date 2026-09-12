from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.models.metadata import HeadingContext

# ============================================================
# STRUCTURAL ELEMENT
# ============================================================


class StructuralElement(BaseModel):

    element_id: str

    element_type: str

    content: str

    heading_context: HeadingContext = Field(default_factory=HeadingContext)

    heading_level: Optional[int] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

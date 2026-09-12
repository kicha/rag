from pydantic import BaseModel

# ============================================================
# DOCUMENT
# ============================================================


class Document(BaseModel):

    document_id: str
    source: str
    text: str

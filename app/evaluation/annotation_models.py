from typing import Optional

from pydantic import BaseModel, Field

# ============================================================
# CHILD ANNOTATION CANDIDATE
# ============================================================


class ChildAnnotationCandidate(BaseModel):
    """
    One actual persisted ChildChunk presented to the annotator.

    suggested_relevance is intentionally None.

    This script organizes evidence for human review. It does
    not automatically decide relevance.
    """

    child_key: str
    child_index: int
    content: str

    suggested_relevance: Optional[int] = None


# ============================================================
# PARENT ANNOTATION CANDIDATE
# ============================================================


class ParentAnnotationCandidate(BaseModel):
    """
    One actual persisted ParentChunk presented to the annotator,
    together with all ChildChunks that belong to it.
    """

    parent_key: str
    parent_index: int
    section_path: list[str]
    content: str
    suggested_relevance: Optional[int] = None
    children: list[ChildAnnotationCandidate] = Field(default_factory=list)


# ============================================================
# DOCUMENT ANNOTATION CANDIDATE
# ============================================================


class DocumentAnnotationCandidate(BaseModel):
    """
    One document inherited from the Benchmark V1 relevance set.

    The legacy dataset tells us that the document was relevant,
    but it does not provide graded relevance.

    Therefore suggested_relevance starts as None.
    """

    document_id: str
    suggested_relevance: Optional[int] = None
    parents: list[ParentAnnotationCandidate] = Field(default_factory=list)


# ============================================================
# QUERY ANNOTATION RECORD
# ============================================================


class QueryAnnotationRecord(BaseModel):
    """
    Human-review workspace for one benchmark query.
    """

    query_id: str
    query: str
    query_class: str
    answerability: str
    annotation_status: str
    documents: list[DocumentAnnotationCandidate] = Field(default_factory=list)

    notes: Optional[str] = None


# ============================================================
# COMPLETE ANNOTATION WORKSPACE
# ============================================================


class AnnotationWorkspace(BaseModel):
    """
    Human-review workspace generated from the frozen Benchmark
    V2 units.

    This is NOT the gold dataset itself.

    It is an annotation aid used to produce the final curated
    gold judgments.
    """

    benchmark_version: str
    corpus_sha256: str
    query_count: int
    records: list[QueryAnnotationRecord]

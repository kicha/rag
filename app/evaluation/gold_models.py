from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

# ============================================================
# RELEVANCE
# ============================================================


class RelevanceGrade(int, Enum):
    """
    Graded relevance used by Benchmark V2.

    The grades are intentionally simple:

        3 = directly answer-bearing
        2 = strongly supporting
        1 = weak/supporting

    Items that do not appear in the gold judgments are treated
    as relevance 0 by the evaluation engine.

    We deliberately do not store thousands of explicit
    relevance=0 judgments.
    """

    WEAK = 1
    SUPPORTING = 2
    DIRECT = 3


# ============================================================
# ANSWERABILITY
# ============================================================


class Answerability(str, Enum):
    """
    Whether the benchmark query can be answered from the
    benchmark corpus.
    """

    ANSWERABLE = "answerable"
    UNANSWERABLE = "unanswerable"


# ============================================================
# ANNOTATION STATUS
# ============================================================


class AnnotationStatus(str, Enum):
    """
    Lifecycle state for an individual gold query.

    MIGRATED:
        Imported from Benchmark V1. Parent/child judgments have
        not yet been manually curated.

    IN_PROGRESS:
        Human annotation has started but is not complete.

    CURATED:
        Document, parent, and child judgments have been reviewed
        and are ready for evaluation.
    """

    MIGRATED = "migrated"
    IN_PROGRESS = "in_progress"
    CURATED = "curated"


class DatasetStatus(str, Enum):
    """
    Lifecycle state for the complete gold dataset.
    """

    DRAFT = "draft"
    FROZEN = "frozen"


# ============================================================
# DOCUMENT JUDGMENT
# ============================================================


class DocumentJudgment(BaseModel):
    """
    Relevance judgment for a document.

    relevance=None is allowed only during migration.

    The old benchmark contains binary document relevance but
    does not tell us whether a relevant document deserves
    relevance grade 1, 2, or 3.

    We therefore preserve the old judgment without inventing
    a graded score.
    """

    document_id: str

    relevance: Optional[RelevanceGrade] = None


# ============================================================
# PARENT JUDGMENT
# ============================================================


class ParentJudgment(BaseModel):
    """
    Relevance judgment for an actual persisted ParentChunk.
    """

    parent_key: str

    relevance: RelevanceGrade


# ============================================================
# CHILD JUDGMENT
# ============================================================


class ChildJudgment(BaseModel):
    """
    Relevance judgment for an actual persisted ChildChunk.
    """

    child_key: str

    relevance: RelevanceGrade


# ============================================================
# GOLD QUERY
# ============================================================


class GoldQueryV2(BaseModel):
    """
    One Benchmark V2 query and its relevance judgments.

    document_judgments:
        broad document-level diagnostic

    parent_judgments:
        primary context-level evaluation target

    child_judgments:
        retrieval precision / candidate quality target
    """

    query_id: str

    query: str

    # Preserve the original benchmark query classification.
    # We do not rename or reinterpret the old `class` value
    # during migration.
    query_class: str

    answerability: Answerability

    annotation_status: AnnotationStatus = AnnotationStatus.MIGRATED

    document_judgments: list[DocumentJudgment] = Field(default_factory=list)

    parent_judgments: list[ParentJudgment] = Field(default_factory=list)

    child_judgments: list[ChildJudgment] = Field(default_factory=list)

    notes: Optional[str] = None

    # --------------------------------------------------------
    # DUPLICATE JUDGMENT VALIDATION
    # --------------------------------------------------------

    @model_validator(mode="after")
    def validate_unique_judgments(
        self,
    ) -> "GoldQueryV2":

        document_ids = [judgment.document_id for judgment in self.document_judgments]

        parent_keys = [judgment.parent_key for judgment in self.parent_judgments]

        child_keys = [judgment.child_key for judgment in self.child_judgments]

        if len(document_ids) != len(set(document_ids)):
            raise ValueError(
                f"Duplicate document judgments " f"for query_id={self.query_id}"
            )

        if len(parent_keys) != len(set(parent_keys)):
            raise ValueError(
                f"Duplicate parent judgments " f"for query_id={self.query_id}"
            )

        if len(child_keys) != len(set(child_keys)):
            raise ValueError(
                f"Duplicate child judgments " f"for query_id={self.query_id}"
            )

        return self

    # --------------------------------------------------------
    # CONVENIENCE METHODS
    # --------------------------------------------------------

    def document_relevance_map(
        self,
    ) -> dict[str, int]:

        return {
            judgment.document_id: (int(judgment.relevance))
            for judgment in self.document_judgments
            if judgment.relevance is not None
        }

    def parent_relevance_map(
        self,
    ) -> dict[str, int]:

        return {
            judgment.parent_key: (int(judgment.relevance))
            for judgment in self.parent_judgments
        }

    def child_relevance_map(
        self,
    ) -> dict[str, int]:

        return {
            judgment.child_key: (int(judgment.relevance))
            for judgment in self.child_judgments
        }


# ============================================================
# GOLD DATASET
# ============================================================


class GoldDatasetV2(BaseModel):
    """
    Complete Benchmark V2 gold dataset.
    """

    schema_version: str = "2.0"

    benchmark_version: str = "2.0"

    corpus_sha256: str

    status: DatasetStatus = DatasetStatus.DRAFT

    queries: list[GoldQueryV2]

    # --------------------------------------------------------
    # DATASET-WIDE VALIDATION
    # --------------------------------------------------------

    @model_validator(mode="after")
    def validate_unique_query_ids(
        self,
    ) -> "GoldDatasetV2":

        query_ids = [query.query_id for query in self.queries]

        if len(query_ids) != len(set(query_ids)):
            raise ValueError("Duplicate query_id values " "detected in gold dataset.")

        return self

    @property
    def query_count(
        self,
    ) -> int:

        return len(self.queries)

    @property
    def curated_query_count(
        self,
    ) -> int:

        return sum(
            1
            for query in self.queries
            if query.annotation_status == AnnotationStatus.CURATED
        )

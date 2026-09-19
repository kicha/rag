import json
import logging
from pathlib import Path
from typing import Any

from app.evaluation.annotation_models import (
    AnnotationWorkspace,
    ChildAnnotationCandidate,
    DocumentAnnotationCandidate,
    ParentAnnotationCandidate,
    QueryAnnotationRecord,
)
from app.evaluation.gold_models import (
    GoldDatasetV2,
)
from app.utils.logging_config import (
    configure_logging,
)

logger = logging.getLogger(__name__)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BENCHMARK_DIRECTORY = PROJECT_ROOT / "data" / "benchmark"

GOLD_DRAFT_PATH = BENCHMARK_DIRECTORY / "gold_queries_v2_draft.json"

UNITS_PATH = BENCHMARK_DIRECTORY / "benchmark_v2_units.json"

JSON_OUTPUT_PATH = BENCHMARK_DIRECTORY / "gold_annotation_candidates_v2.json"

MARKDOWN_OUTPUT_PATH = BENCHMARK_DIRECTORY / "gold_annotation_candidates_v2.md"


# ============================================================
# JSON LOADING
# ============================================================


def load_json(
    path: Path,
) -> Any:
    """
    Load JSON from disk and fail immediately if the expected
    benchmark artifact does not exist.
    """

    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# ANNOTATION CANDIDATE BUILDER
# ============================================================


class GoldAnnotationCandidateBuilder:
    """
    Build a human-review workspace for Benchmark V2.

    Important:

    This class does NOT determine relevance.

    It only narrows the review space by using the legacy
    document-level gold judgments.

    Example:

        Query says DOC-002 is relevant.

        Instead of showing all 120 parents, we show only the
        actual ParentChunks belonging to DOC-002 and their
        ChildChunks.

    Human annotation then decides:

        relevance 3
        relevance 2
        relevance 1
        or irrelevant
    """

    def __init__(
        self,
        dataset: GoldDatasetV2,
        units_data: dict[str, Any],
    ) -> None:

        self.dataset = dataset
        self.units_data = units_data

        # ----------------------------------------------------
        # Build document -> parents lookup once.
        #
        # Without this index we would repeatedly scan all
        # 120 parents for every query.
        # ----------------------------------------------------

        self.parents_by_document_id: dict[
            str,
            list[dict[str, Any]],
        ] = {}

        self._build_unit_indexes()

    # ========================================================
    # UNIT INDEX
    # ========================================================

    def _build_unit_indexes(
        self,
    ) -> None:

        for parent in self.units_data["parents"]:

            document_id = parent["document_id"]

            self.parents_by_document_id.setdefault(
                document_id,
                [],
            ).append(parent)

        # ----------------------------------------------------
        # Ensure deterministic ordering.
        #
        # Annotation files should remain stable between runs
        # as long as the frozen benchmark universe does not
        # change.
        # ----------------------------------------------------

        for parents in self.parents_by_document_id.values():

            parents.sort(key=lambda parent: (parent["parent_index"]))

    # ========================================================
    # PUBLIC BUILD METHOD
    # ========================================================

    def build(
        self,
    ) -> AnnotationWorkspace:

        records: list[QueryAnnotationRecord] = []

        for query in self.dataset.queries:

            record = self._build_query_record(query)

            records.append(record)

        return AnnotationWorkspace(
            benchmark_version=(self.dataset.benchmark_version),
            corpus_sha256=(self.dataset.corpus_sha256),
            query_count=len(records),
            records=records,
        )

    # ========================================================
    # QUERY RECORD
    # ========================================================

    def _build_query_record(
        self,
        query,
    ) -> QueryAnnotationRecord:

        documents: list[DocumentAnnotationCandidate] = []

        # ----------------------------------------------------
        # The migrated document judgments tell us which
        # documents the old benchmark considered relevant.
        #
        # We use those documents only to reduce the annotation
        # search space.
        #
        # We do NOT automatically mark their parents or
        # children as relevant.
        # ----------------------------------------------------

        for document_judgment in query.document_judgments:

            document_id = document_judgment.document_id

            parents = self.parents_by_document_id.get(
                document_id,
                [],
            )

            if not parents:
                raise RuntimeError(
                    f"query_id={query.query_id} "
                    f"references document_id="
                    f"{document_id}, but no "
                    f"ParentChunks were found."
                )

            parent_candidates = [
                self._build_parent_candidate(parent) for parent in parents
            ]

            documents.append(
                DocumentAnnotationCandidate(
                    document_id=document_id,
                    # Legacy document relevance is binary only.
                    # We intentionally do not convert it to a
                    # graded value automatically.
                    suggested_relevance=None,
                    parents=parent_candidates,
                )
            )

        return QueryAnnotationRecord(
            query_id=query.query_id,
            query=query.query,
            query_class=query.query_class,
            answerability=(query.answerability.value),
            annotation_status=(query.annotation_status.value),
            documents=documents,
            notes=query.notes,
        )

    # ========================================================
    # PARENT CANDIDATE
    # ========================================================

    @staticmethod
    def _build_parent_candidate(
        parent: dict[str, Any],
    ) -> ParentAnnotationCandidate:

        children = sorted(
            parent.get(
                "children",
                [],
            ),
            key=lambda child: (child["child_index"]),
        )

        child_candidates = [
            ChildAnnotationCandidate(
                child_key=child["child_key"],
                child_index=child["child_index"],
                content=child["content"],
                suggested_relevance=None,
            )
            for child in children
        ]

        return ParentAnnotationCandidate(
            parent_key=parent["parent_key"],
            parent_index=parent["parent_index"],
            section_path=parent["section_path"],
            content=parent["content"],
            suggested_relevance=None,
            children=child_candidates,
        )


# ============================================================
# MARKDOWN RENDERER
# ============================================================


class AnnotationMarkdownRenderer:
    """
    Produce a human-readable annotation document.

    JSON remains the structured machine-readable workspace.

    Markdown is easier for us to inspect together during the
    curation session.
    """

    @staticmethod
    def render(
        workspace: AnnotationWorkspace,
    ) -> str:

        lines: list[str] = []
        lines.append("# Benchmark V2 Gold Annotation Candidates")
        lines.append("")
        lines.append(f"Benchmark version: " f"{workspace.benchmark_version}")
        lines.append(f"Corpus SHA-256: " f"{workspace.corpus_sha256}")
        lines.append(f"Queries: {workspace.query_count}")
        lines.append("")
        lines.append("Relevance scale:")
        lines.append("- 3 = directly answer-bearing")
        lines.append("- 2 = strongly supporting")
        lines.append("- 1 = weak/supporting")
        lines.append("- blank = irrelevant or not yet annotated")
        lines.append("")

        # ----------------------------------------------------
        # Render every query independently.
        # ----------------------------------------------------

        for record in workspace.records:
            lines.append("---")
            lines.append("")
            lines.append(f"## {record.query_id}")
            lines.append("")
            lines.append(f"**Query:** {record.query}")
            lines.append("")
            lines.append(f"**Query class:** " f"{record.query_class}")
            lines.append("")
            lines.append(f"**Answerability:** " f"{record.answerability}")
            lines.append("")

            if not record.documents:
                lines.append("No relevant documents in the " "legacy benchmark.")
                lines.append("")

                continue

            for document in record.documents:
                lines.append(f"### Document " f"{document.document_id}")
                lines.append("")
                lines.append("**Document relevance:** " "`[   ]`")
                lines.append("")

                for parent in document.parents:
                    section_path = " > ".join(parent.section_path)
                    lines.append(f"#### Parent " f"{parent.parent_index}")
                    lines.append("")
                    lines.append(f"**parent_key:** " f"`{parent.parent_key}`")
                    lines.append("")
                    lines.append(f"**section_path:** " f"{section_path}")
                    lines.append("")
                    lines.append("**Parent relevance:** " "`[   ]`")
                    lines.append("")
                    lines.append(parent.content)
                    lines.append("")

                    # ----------------------------------------
                    # Render children directly below the
                    # parent so their retrieval context is
                    # visually obvious.
                    # ----------------------------------------

                    for child in parent.children:
                        lines.append(f"##### Child " f"{child.child_index}")
                        lines.append("")
                        lines.append(f"**child_key:** " f"`{child.child_key}`")
                        lines.append("")
                        lines.append("**Child relevance:** " "`[   ]`")
                        lines.append("")
                        lines.append(child.content)
                        lines.append("")

        return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    # --------------------------------------------------------
    # Load the migrated gold dataset.
    # --------------------------------------------------------

    gold_data = load_json(GOLD_DRAFT_PATH)

    dataset = GoldDatasetV2.model_validate(gold_data)

    # --------------------------------------------------------
    # Load the actual frozen ParentChunk/ChildChunk universe.
    # --------------------------------------------------------

    units_data = load_json(UNITS_PATH)

    # --------------------------------------------------------
    # Build annotation workspace.
    # --------------------------------------------------------

    builder = GoldAnnotationCandidateBuilder(
        dataset=dataset,
        units_data=units_data,
    )

    workspace = builder.build()

    # --------------------------------------------------------
    # Structured JSON annotation workspace.
    # --------------------------------------------------------

    JSON_OUTPUT_PATH.write_text(
        workspace.model_dump_json(indent=2),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Human-readable Markdown annotation workspace.
    # --------------------------------------------------------

    markdown = AnnotationMarkdownRenderer.render(workspace)

    MARKDOWN_OUTPUT_PATH.write_text(
        markdown,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Summary.
    # --------------------------------------------------------

    answerable_count = sum(
        1 for record in workspace.records if record.answerability == "answerable"
    )

    unanswerable_count = workspace.query_count - answerable_count

    candidate_document_count = sum(
        len(record.documents) for record in workspace.records
    )

    candidate_parent_count = sum(
        len(document.parents)
        for record in workspace.records
        for document in record.documents
    )

    candidate_child_count = sum(
        len(parent.children)
        for record in workspace.records
        for document in record.documents
        for parent in document.parents
    )

    logger.info(f"query_count=" f"{workspace.query_count}")
    logger.info(f"answerable_queries=" f"{answerable_count}")
    logger.info(f"unanswerable_queries=" f"{unanswerable_count}")
    logger.info(f"candidate_documents=" f"{candidate_document_count}")
    logger.info(f"candidate_parents=" f"{candidate_parent_count}")
    logger.info(f"candidate_children=" f"{candidate_child_count}")
    logger.info(f"json_output=" f"{JSON_OUTPUT_PATH}")
    logger.info(f"markdown_output=" f"{MARKDOWN_OUTPUT_PATH}")
    logger.info("Benchmark V2 annotation candidate " "generation PASSED.")


if __name__ == "__main__":

    configure_logging()

    main()

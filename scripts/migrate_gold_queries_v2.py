import json
import logging
from pathlib import Path
from typing import Any

from app.evaluation.gold_models import (
    AnnotationStatus,
    Answerability,
    DocumentJudgment,
    GoldDatasetV2,
    GoldQueryV2,
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
SOURCE_GOLD_PATH = BENCHMARK_DIRECTORY / "gold_queries.json"
MANIFEST_PATH = BENCHMARK_DIRECTORY / "manifest.json"
OUTPUT_PATH = BENCHMARK_DIRECTORY / "gold_queries_v2_draft.json"


# ============================================================
# LOADERS
# ============================================================


def load_json(
    path: Path,
) -> Any:

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def extract_legacy_queries(
    data: Any,
) -> list[dict[str, Any]]:
    """
    Support both historical gold-file layouts:

        [
            {...},
            {...}
        ]

    or:

        {
            "queries": [...]
        }
    """

    if isinstance(
        data,
        list,
    ):
        return data

    if isinstance(data, dict) and isinstance(
        data.get("queries"),
        list,
    ):
        return data["queries"]

    raise RuntimeError("Unsupported legacy gold_queries.json " "structure.")


# ============================================================
# MIGRATION
# ============================================================


def migrate_query(
    legacy_query: dict[str, Any],
    query_index: int,
) -> GoldQueryV2:

    query_text = legacy_query.get("query")

    if not query_text:
        raise ValueError(f"Legacy query at index " f"{query_index} has no query text.")

    relevant_documents = legacy_query.get(
        "relevant_docs",
        [],
    )

    if relevant_documents:

        answerability = Answerability.ANSWERABLE

    else:

        answerability = Answerability.UNANSWERABLE

    # --------------------------------------------------------
    # Preserve legacy document relevance exactly.
    #
    # The original dataset tells us only that the document is
    # relevant. It does not provide graded relevance.
    #
    # Therefore relevance remains None until manual curation.
    # --------------------------------------------------------

    document_judgments = [
        DocumentJudgment(
            document_id=document_id,
            relevance=None,
        )
        for document_id in relevant_documents
    ]

    return GoldQueryV2(
        query_id=(f"Q{query_index:03d}"),
        query=query_text,
        query_class=str(
            legacy_query.get(
                "class",
                "unknown",
            )
        ),
        answerability=answerability,
        annotation_status=(AnnotationStatus.MIGRATED),
        document_judgments=(document_judgments),
        # We intentionally do not invent these.
        parent_judgments=[],
        child_judgments=[],
    )


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    legacy_data = load_json(SOURCE_GOLD_PATH)

    manifest = load_json(MANIFEST_PATH)

    legacy_queries = extract_legacy_queries(legacy_data)

    migrated_queries = [
        migrate_query(
            legacy_query=legacy_query,
            query_index=query_index,
        )
        for query_index, legacy_query in enumerate(
            legacy_queries,
            start=1,
        )
    ]

    dataset = GoldDatasetV2(
        benchmark_version=(manifest["benchmark_version"]),
        corpus_sha256=(manifest["corpus_sha256"]),
        queries=migrated_queries,
    )

    OUTPUT_PATH.write_text(
        dataset.model_dump_json(indent=2),
        encoding="utf-8",
    )

    answerable_count = sum(
        1
        for query in dataset.queries
        if query.answerability == Answerability.ANSWERABLE
    )

    unanswerable_count = dataset.query_count - answerable_count
    logger.info(f"source_queries=" f"{len(legacy_queries)}")
    logger.info(f"migrated_queries=" f"{dataset.query_count}")
    logger.info(f"answerable_queries=" f"{answerable_count}")
    logger.info(f"unanswerable_queries=" f"{unanswerable_count}")
    logger.info(f"curated_queries=" f"{dataset.curated_query_count}")
    logger.info(f"output_path={OUTPUT_PATH}")
    logger.info("Benchmark V2 gold migration PASSED.")


if __name__ == "__main__":

    configure_logging()
    main()

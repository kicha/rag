import logging
from pathlib import Path
from time import perf_counter

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)
from app.ingestion.markdown_corpus_loader import (
    MarkdownCorpusLoader,
)
from app.ingestion.pipeline import (
    StructureAwareRAGDemo,
)
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# ============================================================
# MAIN
# ============================================================


def main() -> None:
    configure_logging()
    logger.info("Starting Benchmark V2 corpus ingestion.")
    config = ChunkingConfig()
    hybrid_config = HybridSearchConfig()
    logger.info(f"documents_directory=" f"{DOCUMENTS_DIR}")
    logger.info(f"mongodb_database=" f"{config.mongodb_database}")
    logger.info(f"mongodb_parent_collection=" f"{config.mongodb_parent_collection}")
    logger.info(f"qdrant_collection=" f"{hybrid_config.collection_name}")

    # ========================================================
    # LOAD DOCUMENTS
    # ========================================================

    loader = MarkdownCorpusLoader(documents_directory=DOCUMENTS_DIR)
    documents = loader.load()
    logger.info(f"documents_discovered=" f"{len(documents)}")
    for document in documents:
        logger.debug(
            f"document_id=" f"{document.document_id} " f"source={document.source}"
        )

    # ========================================================
    # APPLICATION
    # ========================================================

    app = StructureAwareRAGDemo(
        config=config,
        hybrid_config=hybrid_config,
    )

    total_parents = 0
    total_children = 0
    succeeded = 0
    failed = 0

    started = perf_counter()

    try:

        for index, document in enumerate(
            documents,
            start=1,
        ):
            document_started = perf_counter()
            logger.info(
                f"Processing document "
                f"{index}/{len(documents)} "
                f"document_id="
                f"{document.document_id} "
                f"source="
                f"{document.source}"
            )

            try:

                result = app.ingest(
                    document=document,
                    recreate_hybrid_collection=(index == 1),
                )

                elapsed = perf_counter() - document_started
                parent_count = len(result.parents)
                child_count = len(result.children)
                total_parents += parent_count
                total_children += child_count
                succeeded += 1
                logger.info(
                    f"Completed document "
                    f"document_id="
                    f"{document.document_id} "
                    f"parents="
                    f"{parent_count} "
                    f"children="
                    f"{child_count} "
                    f"elapsed_seconds="
                    f"{elapsed:.2f}"
                )

            except Exception:
                failed += 1
                logger.exception(
                    f"Failed document " f"document_id=" f"{document.document_id}"
                )

                raise

    finally:

        app.close()

    total_elapsed = perf_counter() - started

    logger.info(
        f"Corpus ingestion complete "
        f"documents_discovered="
        f"{len(documents)} "
        f"documents_succeeded="
        f"{succeeded} "
        f"documents_failed="
        f"{failed} "
        f"total_parents="
        f"{total_parents} "
        f"total_children="
        f"{total_children} "
        f"elapsed_seconds="
        f"{total_elapsed:.2f} "
        f"mongodb_collection="
        f"{config.mongodb_parent_collection} "
        f"qdrant_collection="
        f"{hybrid_config.collection_name}"
    )


if __name__ == "__main__":

    main()

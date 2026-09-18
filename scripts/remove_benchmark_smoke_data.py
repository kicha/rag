import logging

from app.config.settings import ChunkingConfig
from app.repositories.parent_repository import ParentRepository
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:

    configure_logging()
    config = ChunkingConfig()
    repository = ParentRepository(config)

    try:

        document_id = "DOC-TEST-001"

        count_before = repository.count_by_document_id(document_id)

        logger.info(
            f"document_id={document_id} " f"parents_before_delete={count_before}"
        )

        deleted_count = repository.delete_by_document_id(document_id)

        logger.info(f"document_id={document_id} " f"parents_deleted={deleted_count}")

        count_after = repository.count_by_document_id(document_id)

        logger.info(f"document_id={document_id} " f"parents_after_delete={count_after}")

        if count_after != 0:
            raise RuntimeError(
                f"Smoke-test parents still exist " f"for document_id={document_id}."
            )

        logger.info("Benchmark V2 smoke-data cleanup PASSED.")

    finally:

        repository.close()


if __name__ == "__main__":

    main()

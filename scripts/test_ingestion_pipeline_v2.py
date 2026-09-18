import logging

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)
from app.ingestion.pipeline import (
    StructureAwareRAGDemo,
)
from app.models.document import Document
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:

    document = Document(
        document_id="DOC-TEST-001",
        source="phase_2b_smoke_test.md",
        text="""
# Vector Databases

Vector databases store embeddings for similarity search.

## HNSW

HNSW uses a hierarchical graph for approximate nearest
neighbor search.

### ef_construct

The ef_construct parameter controls the amount of graph
exploration performed during index construction.
""".strip(),
    )

    config = ChunkingConfig()

    hybrid_config = HybridSearchConfig()

    app = StructureAwareRAGDemo(
        config=config,
        hybrid_config=hybrid_config,
    )

    try:

        result = app.ingest(
            document=document,
            recreate_hybrid_collection=True,
        )
        logger.info(f"parents={len(result.parents)}")
        logger.info(f"children={len(result.children)}")

        for parent in result.parents:
            logger.info(f"parent_id=" f"{parent.parent_id}")
            logger.info(f"parent_key=" f"{parent.parent_key}")

        for child in result.children:
            logger.info(f"child_id=" f"{child.child_id}")
            logger.info(f"child_key=" f"{child.child_key}")
            logger.info(f"parent_id=" f"{child.parent_id}")
            logger.info(f"parent_key=" f"{child.parent_key}")

        assert result.parents
        assert result.children

        parent_ids = {parent.parent_id for parent in result.parents}
        parent_keys = {parent.parent_key for parent in result.parents}
        assert all(child.parent_id in parent_ids for child in result.children)
        assert all(child.parent_key in parent_keys for child in result.children)
        logger.info("Phase II-B ingestion " "validation PASSED.")

    finally:

        app.close()


if __name__ == "__main__":
    configure_logging()
    main()

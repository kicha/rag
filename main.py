from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)

from app.ingestion.pipeline import (
    StructureAwareRAGDemo,
)

from scripts.test_parent_chunking import (
    DemoDocumentFactory,
)

# ============================================================
# MAIN
# ============================================================


def main():

    # --------------------------------------------------------
    # STANDARD PROJECT CONFIG
    # --------------------------------------------------------

    config = ChunkingConfig(
        max_chunk_chars=300,
        min_chunk_chars=100,
        child_chunk_chars=120,
        child_overlap_chars=30,
        embedding_model_name=("sentence-transformers/" "all-MiniLM-L6-v2"),
        qdrant_host="localhost",
        qdrant_port=6333,
        collection_name=("structure_aware_v3"),
    )

    # --------------------------------------------------------
    # HYBRID SEARCH CONFIG
    # --------------------------------------------------------

    hybrid_config = HybridSearchConfig(
        collection_name=("structure_aware_v3_hybrid"),
    )

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    app = StructureAwareRAGDemo(
        config=config,
        hybrid_config=hybrid_config,
    )

    try:

        # ----------------------------------------------------
        # DOCUMENT
        # ----------------------------------------------------

        document = DemoDocumentFactory.create()

        # ----------------------------------------------------
        # INGEST
        # ----------------------------------------------------

        result = app.ingest(
            document=document,
            # For our FIRST hybrid experiment we intentionally
            # rebuild the experimental collection so that we
            # know it contains exactly the current 19 children.
            recreate_hybrid_collection=True,
        )

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("INGESTION COMPLETE")
        print("=" * 70)

        print("Parents:", len(result.parents))
        print("Children:", len(result.children))

    finally:

        app.close()


if __name__ == "__main__":
    main()

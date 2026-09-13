from pathlib import Path

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)

from app.embeddings.embedding_service import (
    EmbeddingService,
)

from app.embeddings.sparse_embedding_service import (
    SparseEmbeddingService,
)

from app.evaluation.retrieval_benchmark import (
    GoldQueryLoader,
    RetrievalBenchmarkEvaluator,
)

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_QUERY_PATH = PROJECT_ROOT / "data" / "benchmark" / "gold_queries.json"

OUTPUT_PATH = PROJECT_ROOT / "data" / "benchmark" / "retrieval_benchmark_results.json"


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    print()
    print("=" * 100)
    print("AGENTIC RAG RETRIEVAL BENCHMARK")
    print("=" * 100)

    # ========================================================
    # CONFIG
    # ========================================================

    config = ChunkingConfig()

    hybrid_config = HybridSearchConfig()

    # ========================================================
    # EMBEDDING SERVICES
    # ========================================================

    dense_embedder = EmbeddingService(config.embedding_model_name)

    sparse_embedder = SparseEmbeddingService(
        model_name=(hybrid_config.sparse_model_name)
    )

    vector_size = dense_embedder.model.get_embedding_dimension()

    # ========================================================
    # HYBRID VECTOR STORE
    # ========================================================

    hybrid_store = HybridQdrantStore(
        config=hybrid_config,
        vector_size=vector_size,
        url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
    )

    # ========================================================
    # RETRIEVER
    # ========================================================

    retriever = HybridChildRetriever(
        dense_embedding_service=(dense_embedder),
        sparse_embedding_service=(sparse_embedder),
        vector_store=(hybrid_store),
    )

    # ========================================================
    # LOAD GOLD QUERIES
    # ========================================================

    gold_queries = GoldQueryLoader.load(GOLD_QUERY_PATH)

    print(f"\nGold queries loaded: " f"{len(gold_queries)}")

    # ========================================================
    # EVALUATOR
    # ========================================================

    evaluator = RetrievalBenchmarkEvaluator(
        retriever=retriever,
        vector_store=hybrid_store,
        # ----------------------------------------------
        # Our currently verified benchmark collection.
        # ----------------------------------------------
        expected_point_count=316,
        # ----------------------------------------------
        # Retrieve a broad CHILD pool first.
        #
        # Then collapse those child hits into unique
        # document rankings.
        # ----------------------------------------------
        child_candidate_limit=50,
        # ----------------------------------------------
        # Metrics require top 10 documents.
        # ----------------------------------------------
        document_limit=10,
    )

    # ========================================================
    # RUN
    # ========================================================

    report = evaluator.evaluate(gold_queries=gold_queries)

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    evaluator.print_summary(report)

    # ========================================================
    # SAVE FULL RESULTS
    # ========================================================

    evaluator.save_report(
        report=report,
        output_path=OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()

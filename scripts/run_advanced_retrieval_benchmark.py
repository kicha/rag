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
)

from app.evaluation.advanced_retrieval_benchmark import (
    AdvancedRetrievalBenchmarkEvaluator,
)

from app.repositories.parent_repository import (
    ParentRepository,
)

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

from app.retrieval.hybrid_parent_child_retriever import (
    HybridParentChildRetriever,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_QUERY_PATH = PROJECT_ROOT / "data" / "benchmark" / "gold_queries.json"


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    config = ChunkingConfig()
    hybrid_config = HybridSearchConfig()

    # ========================================================
    # EMBEDDERS
    # ========================================================

    dense_embedder = EmbeddingService(config.embedding_model_name)
    sparse_embedder = SparseEmbeddingService(
        model_name=(hybrid_config.sparse_model_name)
    )

    vector_size = dense_embedder.model.get_embedding_dimension()

    # ========================================================
    # QDRANT
    # ========================================================

    hybrid_store = HybridQdrantStore(
        config=hybrid_config,
        vector_size=vector_size,
        url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
    )

    # ========================================================
    # MONGODB
    # ========================================================

    parent_repository = ParentRepository(config)

    try:

        # ====================================================
        # HYBRID CHILD
        # ====================================================

        hybrid_child_retriever = HybridChildRetriever(
            dense_embedding_service=(dense_embedder),
            sparse_embedding_service=(sparse_embedder),
            vector_store=(hybrid_store),
        )

        # ====================================================
        # HYBRID PARENT EXPANSION
        # ====================================================

        hybrid_parent_retriever = HybridParentChildRetriever(
            hybrid_child_retriever=(hybrid_child_retriever),
            parent_repository=(parent_repository),
        )

        # ====================================================
        # CROSSENCODER
        # ====================================================

        reranker = CrossEncoderReranker()

        # ====================================================
        # FULL PIPELINE
        # ====================================================

        hybrid_rerank_mmr = HybridRerankMMRRetriever(
            hybrid_parent_child_retriever=hybrid_parent_retriever,
            reranker=(reranker),
            embedder=(dense_embedder),
            lambda_mult=0.7,
        )

        # ====================================================
        # GOLD QUERIES
        # ====================================================

        gold_queries = GoldQueryLoader.load(GOLD_QUERY_PATH)

        # ====================================================
        # EVALUATOR
        # ====================================================

        evaluator = AdvancedRetrievalBenchmarkEvaluator(
            hybrid_parent_retriever=(hybrid_parent_retriever),
            cross_encoder=(reranker),
            hybrid_rerank_mmr_retriever=(hybrid_rerank_mmr),
            # broad child pool
            hybrid_child_top_k=30,
            # prune parent candidates
            cross_encoder_top_k=10,
            # final context budget
            final_top_k=3,
        )

        # ====================================================
        # RUN
        # ====================================================

        results = evaluator.evaluate(gold_queries)
        evaluator.print_summary(results)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

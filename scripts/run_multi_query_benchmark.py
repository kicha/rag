import os
from pathlib import Path

from langchain_groq import ChatGroq

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

from app.evaluation.multi_query_benchmark import (
    MultiQueryBenchmarkEvaluator,
)

from app.querying.multi_query_generator import (
    MultiQueryGenerator,
)

from app.repositories.parent_repository import (
    ParentRepository,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

from app.retrieval.hybrid_parent_child_retriever import (
    HybridParentChildRetriever,
)

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

from app.retrieval.multi_query_hybrid_retriever import (
    MultiQueryHybridRetriever,
)

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLD_QUERY_PATH = PROJECT_ROOT / "data" / "benchmark" / "gold_queries.json"


def main() -> None:

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set.")

    # ========================================================
    # CONFIG
    # ========================================================

    config = ChunkingConfig()
    hybrid_config = HybridSearchConfig()

    # ========================================================
    # EMBEDDINGS
    # ========================================================

    dense_embedder = EmbeddingService(config.embedding_model_name)
    vector_size = dense_embedder.model.get_embedding_dimension()
    sparse_embedder = SparseEmbeddingService(
        model_name=(hybrid_config.sparse_model_name)
    )

    # ========================================================
    # QDRANT
    # ========================================================

    hybrid_store = HybridQdrantStore(
        config=(hybrid_config),
        vector_size=(vector_size),
        url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
    )

    hybrid_child_retriever = HybridChildRetriever(
        dense_embedding_service=(dense_embedder),
        sparse_embedding_service=(sparse_embedder),
        vector_store=(hybrid_store),
    )

    # ========================================================
    # MONGODB
    # ========================================================

    parent_repository = ParentRepository(config)

    try:

        # ====================================================
        # BASELINE PARENT RETRIEVER
        # ====================================================

        hybrid_parent_child_retriever = HybridParentChildRetriever(
            hybrid_child_retriever=(hybrid_child_retriever),
            parent_repository=(parent_repository),
        )

        # ====================================================
        # CROSSENCODER
        # ====================================================

        reranker = CrossEncoderReranker()

        # ====================================================
        # BASELINE:
        # HYBRID -> CE -> MMR
        # ====================================================

        baseline_retriever = HybridRerankMMRRetriever(
            hybrid_parent_child_retriever=(hybrid_parent_child_retriever),
            reranker=(reranker),
            embedder=(dense_embedder),
            lambda_mult=0.7,
        )

        # ====================================================
        # MULTI-QUERY GENERATOR
        # ====================================================

        llm = ChatGroq(
            model=("openai/gpt-oss-120b"),
            temperature=0,
            max_retries=2,
        )

        query_generator = MultiQueryGenerator(
            llm=llm,
            generated_query_count=3,
            include_original=True,
            fail_open=True,
        )

        # ====================================================
        # MULTI-QUERY PIPELINE
        # ====================================================

        multi_query_retriever = MultiQueryHybridRetriever(
            query_generator=(query_generator),
            hybrid_child_retriever=(hybrid_child_retriever),
            parent_repository=(parent_repository),
            reranker=(reranker),
            embedder=(dense_embedder),
            lambda_mult=0.7,
            multi_query_rrf_k=60,
        )

        # ====================================================
        # GOLD QUERIES
        # ====================================================

        gold_queries = GoldQueryLoader.load(GOLD_QUERY_PATH)

        print(f"\nGold queries loaded: " f"{len(gold_queries)}")

        # ====================================================
        # EVALUATOR
        # ====================================================

        evaluator = MultiQueryBenchmarkEvaluator(
            hybrid_child_retriever=(hybrid_child_retriever),
            baseline_retriever=(baseline_retriever),
            multi_query_retriever=(multi_query_retriever),
            # Baseline gets 30 child candidates.
            baseline_child_top_k=30,
            # Multi-query:
            # 4 queries × 15 each,
            # then RRF-prune back to 30.
            multi_child_top_k_per_query=15,
            multi_fused_child_top_k=30,
            cross_encoder_top_k=10,
            final_top_k=3,
        )

        report = evaluator.evaluate(gold_queries)
        evaluator.print_summary(report)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

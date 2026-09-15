import os
from pathlib import Path

from langchain_groq import ChatGroq

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)

from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sparse_embedding_service import SparseEmbeddingService
from app.evaluation.retrieval_benchmark import GoldQueryLoader

from app.evaluation.query_rewrite_benchmark import QueryRewriteBenchmarkEvaluator

from app.querying.query_rewriter import (
    QueryRewriter,
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

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY environment " "variable is not set.")

    print()
    print("=" * 110)
    print("QUERY REWRITING RETRIEVAL BENCHMARK")
    print("=" * 110)

    # ========================================================
    # CONFIG
    # ========================================================

    config = ChunkingConfig()

    hybrid_config = HybridSearchConfig()

    # ========================================================
    # DENSE EMBEDDINGS
    # ========================================================

    dense_embedder = EmbeddingService(config.embedding_model_name)

    vector_size = dense_embedder.model.get_embedding_dimension()

    # ========================================================
    # SPARSE EMBEDDINGS
    # ========================================================

    sparse_embedder = SparseEmbeddingService(
        model_name=(hybrid_config.sparse_model_name)
    )

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
        # CHILD RETRIEVER
        # ====================================================

        hybrid_child_retriever = HybridChildRetriever(
            dense_embedding_service=(dense_embedder),
            sparse_embedding_service=(sparse_embedder),
            vector_store=(hybrid_store),
        )

        # ====================================================
        # PARENT EXPANSION
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
        # HYBRID -> CE -> MMR
        # ====================================================

        full_retriever = HybridRerankMMRRetriever(
            hybrid_parent_child_retriever=(hybrid_parent_child_retriever),
            reranker=(reranker),
            embedder=(dense_embedder),
            lambda_mult=0.7,
        )

        # ====================================================
        # QUERY REWRITER LLM
        # ====================================================

        rewrite_llm = ChatGroq(
            model=("openai/gpt-oss-120b"),
            temperature=0,
            max_retries=2,
        )

        query_rewriter = QueryRewriter(
            llm=rewrite_llm,
            fail_open=True,
        )

        # ====================================================
        # GOLD QUERIES
        # ====================================================

        gold_queries = GoldQueryLoader.load(GOLD_QUERY_PATH)

        print(f"\nGold queries loaded: " f"{len(gold_queries)}")

        # ====================================================
        # BENCHMARK
        # ====================================================

        evaluator = QueryRewriteBenchmarkEvaluator(
            query_rewriter=(query_rewriter),
            retriever=(full_retriever),
            # Keep the EXACT same funnel settings
            # as our previous advanced benchmark.
            child_top_k=30,
            cross_encoder_top_k=10,
            final_top_k=3,
        )

        report = evaluator.evaluate(gold_queries)

        evaluator.print_summary(report)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

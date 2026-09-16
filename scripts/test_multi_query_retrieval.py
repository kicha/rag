import os

from langchain_groq import (
    ChatGroq,
)

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

from app.retrieval.multi_query_hybrid_retriever import (
    MultiQueryHybridRetriever,
)

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

# ============================================================
# TEST QUERIES
# ============================================================


TEST_QUERIES = [
    ("How does HNSW avoid " "comparing every vector?"),
    ("Why can multi-query retrieval " "improve recall?"),
    ("What causes a vector " "dimension mismatch?"),
]


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    if not os.getenv("GROQ_API_KEY"):

        raise RuntimeError("GROQ_API_KEY environment " "variable is not set.")

    # ========================================================
    # CONFIG
    # ========================================================

    config = ChunkingConfig()

    hybrid_config = HybridSearchConfig()

    # ========================================================
    # DENSE
    # ========================================================

    dense_embedder = EmbeddingService(config.embedding_model_name)

    vector_size = dense_embedder.model.get_embedding_dimension()

    # ========================================================
    # SPARSE
    # ========================================================

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

    # ========================================================
    # CHILD RETRIEVER
    # ========================================================

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
        # LLM QUERY GENERATOR
        # ====================================================

        llm = ChatGroq(
            model=("openai/gpt-oss-120b"),
            temperature=0,
            max_retries=2,
        )

        query_generator = MultiQueryGenerator(
            llm=llm,
            # 3 alternatives + original
            generated_query_count=3,
            include_original=True,
            fail_open=True,
        )

        # ====================================================
        # CROSSENCODER
        # ====================================================

        reranker = CrossEncoderReranker()

        # ====================================================
        # MULTI-QUERY RETRIEVER
        # ====================================================

        retriever = MultiQueryHybridRetriever(
            query_generator=(query_generator),
            hybrid_child_retriever=(hybrid_child_retriever),
            parent_repository=(parent_repository),
            reranker=(reranker),
            embedder=(dense_embedder),
            lambda_mult=0.7,
            multi_query_rrf_k=60,
        )

        # ====================================================
        # RUN
        # ====================================================

        for query in TEST_QUERIES:

            print()
            print("=" * 70)

            print(f"ORIGINAL QUERY:\n" f"{query}")

            result = retriever.retrieve(
                query=query,
                # each query gets a modest
                # independent child budget
                child_top_k_per_query=15,
                # merged candidate pool
                fused_child_top_k=30,
                cross_encoder_top_k=10,
                final_top_k=3,
            )

            # ================================================
            # GENERATED QUERIES
            # ================================================

            print()
            print("QUERY SET")
            print("-" * 70)

            for index, generated_query in enumerate(
                result.generation.all_queries,
                start=1,
            ):

                marker = "ORIGINAL" if index == 1 else "GENERATED"

                print(f"{index}. " f"[{marker}] " f"{generated_query}")

            # ================================================
            # FUSED CHILDREN
            # ================================================

            print()
            print("TOP FUSED CHILDREN")
            print("-" * 70)

            for rank, child in enumerate(
                result.fused_children[:10],
                start=1,
            ):

                print(
                    f"{rank:>2}. "
                    f"doc={child.document_id:<8} "
                    f"parent={child.parent_id} "
                    f"child={child.child_index:<3} "
                    f"query_hits={child.query_hit_count:<2} "
                    f"mq_rrf="
                    f"{child.multi_query_rrf_score:.6f}"
                )

            # ================================================
            # FINAL PARENTS
            # ================================================

            print()
            print("FINAL PARENTS " "(CrossEncoder -> Parent MMR)")
            print("-" * 70)

            for item in result.final_results:
                print(f"Rank {item.rank}")
                print(f"Document       : " f"{item.parent.document_id}")
                print(f"Parent index   : " f"{item.parent.parent_index}")
                print(f"CE rank        : " f"{item.cross_encoder_rank}")
                print(f"CE score       : " f"{item.cross_encoder_score:.4f}")
                print(f"Query sim      : " f"{item.query_similarity:.4f}")
                print(f"MMR score      : " f"{item.mmr_score:.4f}")
                print("-" * 70)

            print(f"Parents before CE: " f"{result.parent_candidates_before_rerank}")

            print(
                f"Query generation: "
                f"{result.generation.generation_latency_ms:.2f} ms"
            )

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

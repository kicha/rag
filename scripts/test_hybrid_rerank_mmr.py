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

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

# ============================================================
# CONFIG
# ============================================================

config = ChunkingConfig()
hybrid_config = HybridSearchConfig()


# ============================================================
# EMBEDDERS
# ============================================================

dense_embedder = EmbeddingService(config.embedding_model_name)

sparse_embedder = SparseEmbeddingService(hybrid_config.sparse_model_name)


# ============================================================
# VECTOR STORE
# ============================================================

vector_size = dense_embedder.model.get_embedding_dimension()

hybrid_store = HybridQdrantStore(
    config=hybrid_config,
    vector_size=vector_size,
    url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
)


# ============================================================
# REPOSITORY
# ============================================================

parent_repository = ParentRepository(config)


# ============================================================
# HYBRID CHILD RETRIEVER
# ============================================================

hybrid_child_retriever = HybridChildRetriever(
    dense_embedding_service=(dense_embedder),
    sparse_embedding_service=(sparse_embedder),
    vector_store=hybrid_store,
)


# ============================================================
# HYBRID PARENT RETRIEVER
# ============================================================

hybrid_parent_retriever = HybridParentChildRetriever(
    hybrid_child_retriever=(hybrid_child_retriever),
    parent_repository=(parent_repository),
)


# ============================================================
# CROSS ENCODER
# ============================================================

reranker = CrossEncoderReranker()


# ============================================================
# FINAL RETRIEVER
# ============================================================

retriever = HybridRerankMMRRetriever(
    hybrid_parent_child_retriever=(hybrid_parent_retriever),
    reranker=reranker,
    embedder=dense_embedder,
    lambda_mult=0.7,
)


# ============================================================
# QUERY
# ============================================================

query = "How does HNSW search efficiently?"


try:

    results = retriever.retrieve(
        query=query,
        child_top_k=15,
        cross_encoder_top_k=5,
        final_top_k=3,
    )

    print()
    print("=" * 90)
    print("HYBRID -> CROSSENCODER -> " "PARENT MMR")
    print("=" * 90)
    print(f"\nQuery: {query}")
    print(f"Final parents: {len(results)}")

    for result in results:

        parent = result.parent

        print()
        print("-" * 90)
        print(f"FINAL RANK          : " f"{result.rank}")
        print(f"PARENT INDEX        : " f"{parent.parent_index}")
        print(f"PARENT ID           : " f"{parent.parent_id}")
        print(f"CROSSENCODER RANK   : " f"{result.cross_encoder_rank}")
        print(f"CROSSENCODER SCORE  : " f"{result.cross_encoder_score:.6f}")
        print(f"DENSE QUERY SIM     : " f"{result.query_similarity:.6f}")
        print(f"MAX REDUNDANCY      : " f"{result.max_redundancy:.6f}")
        print(f"RELEVANCE CONTRIB   : " f"{result.relevance_contribution:.6f}")
        print(f"REDUNDANCY PENALTY  : " f"{result.redundancy_penalty:.6f}")
        print(f"FINAL MMR SCORE     : " f"{result.mmr_score:.6f}")
        print()
        print(f"CONTENT:\n" f"{parent.content}")

finally:

    parent_repository.close()

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

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

# ============================================================
# CONFIG
# ============================================================

config = ChunkingConfig()
hybrid_config = HybridSearchConfig()

# ============================================================
# EMBEDDING SERVICES
# ============================================================

dense_embedder = EmbeddingService(config.embedding_model_name)
sparse_embedder = SparseEmbeddingService(model_name=hybrid_config.sparse_model_name)


# ============================================================
# VECTOR STORE
#
# IMPORTANT:
# We are NOT recreating or inserting anything here.
#
# main.py / pipeline.py already populated
# structure_aware_v3_hybrid.
# ============================================================

vector_size = dense_embedder.model.get_embedding_dimension()

hybrid_store = HybridQdrantStore(
    config=hybrid_config,
    vector_size=vector_size,
    url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = HybridChildRetriever(
    dense_embedding_service=dense_embedder,
    sparse_embedding_service=sparse_embedder,
    vector_store=hybrid_store,
)


# ============================================================
# QUERIES
# ============================================================

# queries = [
#     "ef_construct",
#     "What does ef_construct control?",
#     "M parameter",
#     "How does the M parameter affect HNSW?",
#     "metadata",
#     "What metadata can be stored with vectors?",
#     "How does HNSW search efficiently?",
# ]

queries = [
    # Semantic paraphrase WITHOUT the exact technical term
    "How can I improve graph quality during index construction?",
    # Natural-language query containing the exact term
    "What does ef_construct control?",
    # Exact lexical query
    "ef_construct",
]

# ============================================================
# RESULT PRINTER
# ============================================================


def print_results(title, results):

    print()
    print("=" * 90)
    print(title)
    print("=" * 90)

    if not results:
        print("No results.")
        return

    for rank, point in enumerate(results, start=1):

        payload = point.payload or {}
        content = payload.get("content", "N/A")
        parent_id = payload.get("parent_id", "N/A")
        child_index = payload.get("child_index", "N/A")

        print(f"\nRank        : {rank}")
        print(f"Score       : {point.score:.6f}")
        print(f"Parent ID   : {parent_id}")
        print(f"Child Index : {child_index}")
        print(f"Content     : {content[:300]}")


# ============================================================
# RUN EXPERIMENT
# ============================================================


for query in queries:

    print()
    print()
    print("#" * 100)
    print(f"QUERY: {query}")
    print("#" * 100)

    # --------------------------------------------------------
    # DENSE
    # --------------------------------------------------------

    dense_results = retriever.retrieve_dense(query=query, limit=5)

    # --------------------------------------------------------
    # SPARSE
    # --------------------------------------------------------

    sparse_results = retriever.retrieve_sparse(query=query, limit=5)

    # --------------------------------------------------------
    # HYBRID
    # --------------------------------------------------------

    hybrid_results = retriever.retrieve_hybrid(query=query, limit=5)

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print_results("DENSE RESULTS", dense_results)
    print_results("SPARSE RESULTS", sparse_results)
    print_results("HYBRID RESULTS", hybrid_results)

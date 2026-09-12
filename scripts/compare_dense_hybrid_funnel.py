from collections import defaultdict

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

# ============================================================
# CONFIG
# ============================================================

config = ChunkingConfig()

hybrid_config = HybridSearchConfig()


# ============================================================
# SERVICES
# ============================================================

dense_embedder = EmbeddingService(config.embedding_model_name)

sparse_embedder = SparseEmbeddingService(model_name=hybrid_config.sparse_model_name)

vector_size = dense_embedder.model.get_embedding_dimension()

hybrid_store = HybridQdrantStore(
    config=hybrid_config,
    vector_size=vector_size,
    url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
)

parent_repository = ParentRepository(config)

retriever = HybridChildRetriever(
    dense_embedding_service=dense_embedder,
    sparse_embedding_service=sparse_embedder,
    vector_store=hybrid_store,
)


# ============================================================
# HELPERS
# ============================================================


def print_child_candidates(
    title: str,
    results,
) -> None:

    print()
    print("=" * 100)
    print(title)
    print("=" * 100)

    for rank, point in enumerate(
        results,
        start=1,
    ):

        payload = point.payload or {}

        print(f"\nRank        : {rank}")

        print(f"Score       : " f"{float(point.score):.6f}")

        print(f"Parent ID   : " f"{payload.get('parent_id')}")

        print(f"Child Index : " f"{payload.get('child_index')}")

        content = payload.get(
            "content",
            "",
        )

        print(f"Content     : " f"{content[:180]}")


def build_parent_summary(
    results,
):
    """
    Collapse child hits into one entry per parent.

    We preserve:
    - best child score
    - matched child count
    - child indexes
    """

    grouped = defaultdict(list)

    for point in results:

        payload = point.payload or {}

        parent_id = payload.get("parent_id")

        if not parent_id:
            continue

        grouped[parent_id].append(
            {
                "score": float(point.score),
                "child_index": payload.get(
                    "child_index",
                    -1,
                ),
            }
        )

    summaries = []

    for (
        parent_id,
        child_hits,
    ) in grouped.items():

        child_hits.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        parent = parent_repository.get_by_id(parent_id)

        if parent is None:

            raise RuntimeError("Dangling parent reference: " f"{parent_id}")

        summaries.append(
            {
                "parent_id": parent_id,
                "parent_index": parent.parent_index,
                "best_score": child_hits[0]["score"],
                "matched_children": len(child_hits),
                "child_indexes": [hit["child_index"] for hit in child_hits],
            }
        )

    summaries.sort(
        key=lambda item: item["best_score"],
        reverse=True,
    )

    return summaries


def print_parent_summary(
    title: str,
    summaries,
) -> None:

    print()
    print("=" * 100)
    print(title)
    print("=" * 100)

    for rank, item in enumerate(
        summaries,
        start=1,
    ):

        print(f"\nRank             : {rank}")

        print(f"Parent Index     : " f"{item['parent_index']}")

        print(f"Parent ID        : " f"{item['parent_id']}")

        print(f"Best Child Score : " f"{item['best_score']:.6f}")

        print(f"Matched Children : " f"{item['matched_children']}")

        print(f"Child Indexes    : " f"{item['child_indexes']}")


def compare_sets(
    dense_parents,
    hybrid_parents,
) -> None:

    dense_ids = {item["parent_id"] for item in dense_parents}

    hybrid_ids = {item["parent_id"] for item in hybrid_parents}

    common = dense_ids & hybrid_ids

    dense_only = dense_ids - hybrid_ids

    hybrid_only = hybrid_ids - dense_ids

    print()
    print("=" * 100)
    print("PARENT CANDIDATE SET COMPARISON")
    print("=" * 100)

    print(f"\nDense unique parents  : " f"{len(dense_ids)}")

    print(f"Hybrid unique parents : " f"{len(hybrid_ids)}")

    print(f"Common parents        : " f"{len(common)}")

    print(f"Dense-only parents    : " f"{len(dense_only)}")

    print(f"Hybrid-only parents   : " f"{len(hybrid_only)}")

    print(f"\nDense-only IDs  : " f"{dense_only}")

    print(f"Hybrid-only IDs : " f"{hybrid_only}")


# ============================================================
# EXPERIMENT
# ============================================================

queries = [
    "ef_construct",
    "How does HNSW search efficiently?",
]


try:

    for query in queries:

        print()
        print()
        print("#" * 100)
        print(f"QUERY: {query}")
        print("#" * 100)

        # ----------------------------------------------------
        # DENSE CHILD CANDIDATES
        # ----------------------------------------------------

        dense_results = retriever.retrieve_dense(
            query=query,
            limit=15,
        )

        # ----------------------------------------------------
        # HYBRID CHILD CANDIDATES
        # ----------------------------------------------------

        hybrid_results = retriever.retrieve_hybrid(
            query=query,
            limit=15,
        )

        # ----------------------------------------------------
        # CHILD-LEVEL VISIBILITY
        # ----------------------------------------------------

        print_child_candidates(
            "DENSE CHILD CANDIDATES",
            dense_results,
        )

        print_child_candidates(
            "HYBRID CHILD CANDIDATES",
            hybrid_results,
        )

        # ----------------------------------------------------
        # COLLAPSE INTO UNIQUE PARENTS
        # ----------------------------------------------------

        dense_parents = build_parent_summary(dense_results)

        hybrid_parents = build_parent_summary(hybrid_results)

        print_parent_summary(
            "DENSE UNIQUE PARENTS",
            dense_parents,
        )

        print_parent_summary(
            "HYBRID UNIQUE PARENTS",
            hybrid_parents,
        )

        # ----------------------------------------------------
        # DIRECT SET COMPARISON
        # ----------------------------------------------------

        compare_sets(
            dense_parents,
            hybrid_parents,
        )

finally:

    parent_repository.close()

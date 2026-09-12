from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.repositories.parent_repository import (
    ParentRepository,
)
from app.retrieval.parent_child_retriever import (
    ParentChildRetriever,
)
from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)
from app.vectorstore.qdrant_store import (
    QdrantVectorStore,
)

# ============================================================
# APPLICATION
# ============================================================


def main() -> None:

    config = ChunkingConfig()

    # ========================================================
    # EMBEDDING MODEL
    # ========================================================

    embedder = EmbeddingService(config.embedding_model_name)

    vector_size = embedder.model.get_embedding_dimension()

    # ========================================================
    # VECTOR STORE
    # ========================================================

    vector_store = QdrantVectorStore(
        config=config,
        vector_size=vector_size,
    )

    # ========================================================
    # PARENT REPOSITORY
    # ========================================================

    parent_repository = ParentRepository(config=config)

    try:

        # ====================================================
        # PARENT / CHILD RETRIEVER
        # ====================================================

        retriever = ParentChildRetriever(
            config=config,
            embedder=embedder,
            vector_store=vector_store,
            parent_repository=(parent_repository),
        )

        # ====================================================
        # CROSS-ENCODER
        # ====================================================

        reranker = CrossEncoderReranker()

        # ====================================================
        # QUERY
        # ====================================================

        # query = "What metadata can be stored with vectors?"
        # query = "How does the M parameter affect HNSW?"
        # query = "How does HNSW search efficiently?"
        query = (
            "Why does HNSW avoid comparing the query "
            "against every vector in the database?"
        )

        print()
        print("=" * 72)
        print("VECTOR RETRIEVAL " "VS CROSS-ENCODER RERANKING")
        print("=" * 72)

        print()
        print(f"QUERY: {query}")

        # ====================================================
        # IMPORTANT:
        #
        # For reranking, retrieve MORE candidates first.
        #
        # Do not use parent_top_k=2 before reranking because
        # doing that could discard a useful candidate before
        # the CrossEncoder ever sees it.
        # ====================================================

        candidates = retriever.retrieve(
            query=query,
            child_top_k=10,
            child_score_threshold=0.0,
            parent_top_k=10,
        )

        # ====================================================
        # VECTOR RANKING
        # ====================================================

        print()
        print("=" * 72)
        print("STAGE 1 — VECTOR RETRIEVAL")
        print("=" * 72)

        for rank, candidate in enumerate(
            candidates,
            start=1,
        ):

            print()
            print(f"VECTOR RANK {rank}")
            print(f"Vector score : " f"{candidate.best_score:.4f}")
            print(f"Parent index : " f"{candidate.parent.parent_index}")
            print(
                f"Section      : "
                f"{candidate.parent.heading_context.get_section_path()}"
            )
            print(f"Content      : " f"{candidate.parent.content}")

        # ====================================================
        # CROSS-ENCODER RERANK
        # ====================================================

        reranked = reranker.rerank(
            query=query,
            candidates=candidates,
            top_k=3,
        )

        # ====================================================
        # RERANKED OUTPUT
        # ====================================================

        print()
        print("=" * 72)
        print("STAGE 2 — CROSS-ENCODER " "RERANKING")
        print("=" * 72)

        print()
        print(f"Candidates reranked : " f"{reranked.candidate_count}")

        print(f"Parents returned    : " f"{reranked.returned_count}")

        for item in reranked.results:

            parent = item.result.parent
            print()
            print("-" * 72)

            print(f"Original vector rank : " f"{item.original_rank}")
            print(f"New reranked rank     : " f"{item.reranked_rank}")
            print(f"Vector score          : " f"{item.vector_score:.4f}")
            print(f"Reranker score        : " f"{item.reranker_score:.4f}")
            print(f"Parent index          : " f"{parent.parent_index}")
            print(
                f"Section               : "
                f"{parent.heading_context.get_section_path()}"
            )

            print()
            print("PARENT CONTENT")

            print(parent.content)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

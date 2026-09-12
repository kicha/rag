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
from app.vectorstore.qdrant_store import (
    QdrantVectorStore,
)

# ============================================================
# RETRIEVAL DEMO
# ============================================================


def main() -> None:

    config = ChunkingConfig()

    # --------------------------------------------------------
    # EMBEDDING SERVICE
    # --------------------------------------------------------

    embedder = EmbeddingService(config.embedding_model_name)

    vector_size = embedder.model.get_embedding_dimension()

    # --------------------------------------------------------
    # QDRANT
    # --------------------------------------------------------

    vector_store = QdrantVectorStore(
        config=config,
        vector_size=vector_size,
    )

    # --------------------------------------------------------
    # MONGODB
    # --------------------------------------------------------

    parent_repository = ParentRepository(config)

    try:

        # ----------------------------------------------------
        # RETRIEVER
        # ----------------------------------------------------

        retriever = ParentChildRetriever(
            config=config,
            embedder=embedder,
            vector_store=vector_store,
            parent_repository=parent_repository,
        )

        # ----------------------------------------------------
        # QUERY
        # ----------------------------------------------------

        query = "How does HNSW search efficiently?"

        print()
        print("=" * 70)
        print("PARENT / CHILD RETRIEVAL")
        print("=" * 70)

        print()
        print(f"QUERY: {query}")

        print()
        print("Retrieval configuration")
        print("-" * 70)
        print(f"Child top-k          : {config.child_top_k}")
        print(f"Child score threshold: {config.child_score_threshold}")
        print(f"Parent top-k         : {config.parent_top_k}")

        results = retriever.retrieve(
            query=query,
            # child_top_k=5,
            # child_score_threshold=0.40,
            # parent_top_k=2,
        )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        print()
        print(f"Unique parents retrieved: " f"{len(results)}")

        for rank, result in enumerate(
            results,
            start=1,
        ):

            parent = result.parent

            print()
            print("=" * 70)
            print(f"PARENT RANK {rank}")
            print("=" * 70)

            print(f"Parent ID     : " f"{parent.parent_id}")
            print(f"Parent index  : " f"{parent.parent_index}")
            print(f"Best score    : " f"{result.best_score:.4f}")
            print(f"Section       : " f"{parent.metadata.section_path}")
            print(f"Matched child : " f"{len(result.matched_children)}")

            # --------------------------------------------
            # CHILD EVIDENCE
            # --------------------------------------------

            for child in result.matched_children:

                print()
                print(f"  Child index : " f"{child.child_index}")
                print(f"  Score       : " f"{child.score:.4f}")
                print(f"  Content     : " f"{child.content!r}")

            # --------------------------------------------
            # FULL PARENT CONTEXT
            # --------------------------------------------

            print()
            print("FULL PARENT CONTEXT")
            print("-" * 70)
            print(parent.content)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

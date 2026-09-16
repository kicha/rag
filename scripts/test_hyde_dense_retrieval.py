from langchain_groq import ChatGroq

from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import EmbeddingService
from app.retrieval.hyde.hyde_generator import HyDEGenerator
from app.retrieval.hyde.hyde_retriever import HyDERetriever
from app.vectorstore.qdrant_store import QdrantVectorStore


def print_results(
    title: str,
    results,
):
    print("\n" + title)
    print("-" * 80)

    if not results:
        print("No results.")
        return

    for rank, result in enumerate(results, start=1):

        print(f"\nRank {rank}")

        # Adapt these fields to however your Qdrant search
        # currently returns results.

        if hasattr(result, "score"):
            print(f"Score : {result.score:.4f}")

        if hasattr(result, "payload"):
            payload = result.payload or {}

            print(
                "Child ID:",
                payload.get("child_id"),
            )

            print(
                "Parent ID:",
                payload.get("parent_id"),
            )

            print(
                "Section:",
                payload.get("section_path"),
            )

            content = payload.get("content", "")

            print(
                "Content:",
                content[:300],
            )


def main():

    # ============================================================
    # CONFIGURATION
    # ============================================================

    config = ChunkingConfig()

    # ============================================================
    # EMBEDDING SERVICE
    # ============================================================

    embedding_service = EmbeddingService(config.embedding_model_name)
    vector_size = embedding_service.model.get_embedding_dimension()

    # ============================================================
    # VECTOR STORE
    # ============================================================

    vector_store = QdrantVectorStore(
        config=config,
        vector_size=vector_size,
    )

    # ============================================================
    # LLM
    # ============================================================

    llm = ChatGroq(
        # model="llama-3.3-70b-versatile",
        model="openai/gpt-oss-120b",
        temperature=0.0,
    )

    # ============================================================
    # HYDE
    # ============================================================

    hyde_generator = HyDEGenerator(
        llm=llm,
    )

    hyde_retriever = HyDERetriever(
        hyde_generator=hyde_generator,
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    # ============================================================
    # TEST QUERIES
    # ============================================================

    queries = [
        "What does ef_construct control?",
        "How does the M parameter affect HNSW?",
        "What metadata can be stored with vectors?",
        "Why does HNSW avoid comparing every vector?",
    ]

    # ============================================================
    # EXPERIMENT
    # ============================================================

    for query in queries:

        print("\n")
        print("=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        # --------------------------------------------------------
        # BASELINE:
        # Original query → embedding → dense retrieval
        # --------------------------------------------------------

        original_embedding = embedding_service.embed_query(query)

        original_results = vector_store.search(
            query_vector=original_embedding,
            top_k=5,
        )

        print_results(
            title="ORIGINAL DENSE RETRIEVAL",
            results=original_results,
        )

        # --------------------------------------------------------
        # HYDE:
        # Query → hypothetical document → embedding → retrieval
        # --------------------------------------------------------

        hyde_result, hyde_results = hyde_retriever.retrieve(
            query=query,
            top_k=5,
        )

        print("\nHYPOTHETICAL DOCUMENT")
        print("-" * 80)
        print(hyde_result.hypothetical_document)

        print_results(
            title="HYDE DENSE RETRIEVAL",
            results=hyde_results,
        )


if __name__ == "__main__":
    main()

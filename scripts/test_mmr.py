from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.retrieval.mmr_retriever import (
    MMRCandidate,
    MMRRetriever,
)
import numpy as np

# ============================================================
# APPLICATION
# ============================================================


def main() -> None:

    embedder = EmbeddingService("sentence-transformers/" "all-MiniLM-L6-v2")

    query = "How does HNSW search efficiently?"

    documents = [
        ("A", "HNSW uses multiple graph layers " "to search vectors efficiently."),
        (
            "B",
            "HNSW search uses hierarchical "
            "graph layers for efficient "
            "nearest-neighbor search.",
        ),
        (
            "C",
            "Search starts at upper HNSW "
            "layers and progressively moves "
            "toward lower layers.",
        ),
        (
            "D",
            "The M parameter controls how "
            "many graph connections each "
            "HNSW node maintains.",
        ),
        (
            "E",
            "Metadata filters can restrict "
            "vector search by source or "
            "document identifier.",
        ),
    ]

    # ========================================================
    # QUERY EMBEDDING
    # ========================================================

    query_embedding = embedder.embed_query(query)

    # ========================================================
    # DOCUMENT EMBEDDINGS
    # ========================================================

    texts = [text for _, text in documents]

    embeddings = embedder.embed_documents(texts)

    # ========================================================
    # BUILD CANDIDATES
    # ========================================================

    candidates = []

    # for (document_id, text), embedding in zip(documents, embeddings):

    #     similarity = MMRRetriever._cosine_similarity(
    #         query_embedding,
    #         embedding,
    #     )

    #     candidates.append(
    #         MMRCandidate(
    #             id=document_id,
    #             content=text,
    #             query_similarity=(similarity),
    #             embedding=(
    #                 embedding.tolist()
    #                 if hasattr(
    #                     embedding,
    #                     "tolist",
    #                 )
    #                 else list(embedding)
    #             ),
    #         )
    #     )

    for (document_id, text), embedding in zip(documents, embeddings):

        query_vector = np.array(
            query_embedding,
            dtype=np.float32,
        )

        document_vector = np.array(
            embedding,
            dtype=np.float32,
        )

        similarity = MMRRetriever._cosine_similarity(
            query_vector,
            document_vector,
        )

        candidates.append(
            MMRCandidate(
                id=document_id,
                content=text,
                query_similarity=similarity,
                embedding=document_vector.tolist(),
            )
        )

    # ========================================================
    # SIMILARITY ORDER
    # ========================================================

    similarity_results = sorted(
        candidates,
        key=lambda item: item.query_similarity,
        reverse=True,
    )

    print()
    print("=" * 72)
    print("PLAIN SIMILARITY RANKING")
    print("=" * 72)

    for rank, item in enumerate(
        similarity_results,
        start=1,
    ):

        print()
        print(f"Rank       : {rank}")
        print(f"Document   : {item.id}")
        print(f"Similarity : " f"{item.query_similarity:.4f}")
        print(f"Content    : " f"{item.content}")

    # ========================================================
    # MMR
    # ========================================================

    mmr = MMRRetriever(lambda_mult=0.2)

    results = mmr.select(
        candidates=candidates,
        top_k=3,
    )

    print()
    print("=" * 72)
    print("MMR RANKING")
    print("=" * 72)

    print()
    print(f"Lambda: {mmr.lambda_mult}")

    for item in results:

        print()
        print(f"Rank             : {item.rank}")
        print(f"Document         : {item.id}")
        print(f"Query similarity : {item.query_similarity:.4f}")
        print(f"Max redundancy   : {item.max_redundancy:.4f}")
        print(f"Relevance contribution : {item.relevance_contribution:.4f}")
        print(f"Redundancy penalty     : {item.redundancy_penalty:.4f}")
        print(f"MMR score        : {item.mmr_score:.4f}")
        print(f"Content          : {item.content}")


if __name__ == "__main__":
    main()

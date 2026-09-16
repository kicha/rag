from typing import Any

from app.embeddings.embedding_service import EmbeddingService
from app.retrieval.hyde.hyde_generator import HyDEGenerator


class HyDERetriever:
    """
    Converts a user query into a hypothetical document using HyDE,
    embeds that hypothetical document, and performs dense retrieval.

    This class does NOT:
    - perform parent expansion
    - rerank with CrossEncoder
    - apply MMR
    - perform sparse retrieval
    - perform RRF

    It is intentionally limited to HyDE-based dense child retrieval.
    """

    def __init__(
        self,
        hyde_generator: HyDEGenerator,
        embedding_service: EmbeddingService,
        vector_store: Any,
    ):
        self.hyde_generator = hyde_generator
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        # ---------------------------------------------------------
        # STEP 1
        # Generate hypothetical document
        # ---------------------------------------------------------

        hyde_result = self.hyde_generator.generate(query)

        hypothetical_document = hyde_result.hypothetical_document

        # ---------------------------------------------------------
        # STEP 2
        # Embed the hypothetical document
        # ---------------------------------------------------------

        hyde_embedding = self.embedding_service.embed_query(hypothetical_document)

        # ---------------------------------------------------------
        # STEP 3
        # Dense retrieval against CHILD chunks
        # ---------------------------------------------------------

        results = self.vector_store.search(
            query_vector=hyde_embedding,
            top_k=top_k,
        )

        return hyde_result, results

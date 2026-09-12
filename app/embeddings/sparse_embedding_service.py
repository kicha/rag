from typing import List

from fastembed import SparseTextEmbedding
from qdrant_client.models import SparseVector


class SparseEmbeddingService:
    """
    Generates sparse lexical embeddings.

    Initial implementation: Qdrant/bm25

    Dense embeddings continue to be handled independently
    by our existing EmbeddingService.
    """

    def __init__(self, model_name: str = "Qdrant/bm25"):
        self.model_name = model_name

        print(f"Loading sparse embedding model: " f"{self.model_name}")

        self.model = SparseTextEmbedding(
            model_name=self.model_name,
        )

    # ---------------------------------------------------------
    # INTERNAL CONVERSION
    # ---------------------------------------------------------

    @staticmethod
    def _to_qdrant_sparse_vector(embedding) -> SparseVector:

        return SparseVector(
            indices=embedding.indices.tolist(),
            values=embedding.values.tolist(),
        )

    # ---------------------------------------------------------
    # DOCUMENT EMBEDDINGS
    # ---------------------------------------------------------

    def embed_documents(self, texts: List[str]) -> List[SparseVector]:

        if not texts:
            return []

        sparse_embeddings = list(self.model.embed(texts))

        return [
            self._to_qdrant_sparse_vector(embedding) for embedding in sparse_embeddings
        ]

    # ---------------------------------------------------------
    # QUERY EMBEDDING
    # ---------------------------------------------------------

    def embed_query(self, query: str) -> SparseVector:

        query = query.strip()

        if not query:
            raise ValueError("Query must not be empty.")

        embeddings = list(self.model.embed([query]))

        if not embeddings:
            raise RuntimeError("Sparse embedding model returned no vector.")

        return self._to_qdrant_sparse_vector(embeddings[0])

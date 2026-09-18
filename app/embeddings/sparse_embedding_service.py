import logging

from fastembed import SparseTextEmbedding
from qdrant_client.models import SparseVector

logger = logging.getLogger(__name__)


class SparseEmbeddingService:
    """
    Generates sparse lexical embeddings.

    Dense embeddings are handled independently by
    EmbeddingService.
    """

    def __init__(self, model_name: str = "Qdrant/bm25") -> None:

        self.model_name = model_name
        logger.info(f"Loading sparse embedding model: {self.model_name}")

        self.model = SparseTextEmbedding(
            model_name=self.model_name,
        )

    @staticmethod
    def _to_qdrant_sparse_vector(embedding) -> SparseVector:

        return SparseVector(
            indices=embedding.indices.tolist(),
            values=embedding.values.tolist(),
        )

    def embed_documents(self, texts: list[str]) -> list[SparseVector]:

        if not texts:
            return []

        sparse_embeddings = list(self.model.embed(texts))

        return [
            self._to_qdrant_sparse_vector(embedding) for embedding in sparse_embeddings
        ]

    def embed_query(self, query: str) -> SparseVector:

        query = query.strip()

        if not query:
            raise ValueError("Query must not be empty.")

        embeddings = list(self.model.embed([query]))

        if not embeddings:
            raise RuntimeError("Sparse embedding model returned no vector.")

        return self._to_qdrant_sparse_vector(embeddings[0])

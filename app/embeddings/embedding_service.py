import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


# ============================================================
# EMBEDDING SERVICE
# ============================================================


class EmbeddingService:

    def __init__(self, model_name: str) -> None:

        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(texts, normalize_embeddings=True)

        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:

        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

        embedding = self.model.encode(query, normalize_embeddings=True)

        return embedding.tolist()

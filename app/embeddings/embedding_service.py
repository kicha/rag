from typing import List
from sentence_transformers import SentenceTransformer

# ============================================================
# EMBEDDING SERVICE
# ============================================================


class EmbeddingService:

    def __init__(
        self,
        model_name: str,
    ):

        print(f"\nLoading embedding model: " f"{model_name}")

        self.model = SentenceTransformer(model_name)

    # def embed(
    #     self,
    #     texts: List[str],
    # ):

    #     return self.model.encode(
    #         texts,
    #         normalize_embeddings=True,
    #         show_progress_bar=True,
    #     )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    # def embed_query(
    #     self,
    #     query: str,
    # ):

    #     return self.model.encode(
    #         query,
    #         normalize_embeddings=True,
    #     )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()

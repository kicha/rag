from typing import List

from qdrant_client.models import ScoredPoint

from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.embeddings.sparse_embedding_service import (
    SparseEmbeddingService,
)
from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)


class HybridChildRetriever:

    def __init__(
        self,
        dense_embedding_service: EmbeddingService,
        sparse_embedding_service: SparseEmbeddingService,
        vector_store: HybridQdrantStore,
    ):
        self.dense_embedding_service = dense_embedding_service
        self.sparse_embedding_service = sparse_embedding_service
        self.vector_store = vector_store

    # =========================================================
    # DENSE
    # =========================================================

    def retrieve_dense(
        self,
        query: str,
        limit: int = 10,
    ) -> List[ScoredPoint]:

        self._validate_query(query)

        dense_vector = self.dense_embedding_service.embed_query(query)

        return self.vector_store.dense_search(
            query_vector=dense_vector,
            limit=limit,
        )

    # =========================================================
    # SPARSE
    # =========================================================

    def retrieve_sparse(self, query: str, limit: int = 10) -> List[ScoredPoint]:

        self._validate_query(query)

        sparse_vector = self.sparse_embedding_service.embed_query(query)

        return self.vector_store.sparse_search(
            query_vector=sparse_vector,
            limit=limit,
        )

    # =========================================================
    # HYBRID
    # =========================================================

    def retrieve_hybrid(self, query: str, limit: int = 10) -> List[ScoredPoint]:

        self._validate_query(query)

        dense_vector = self.dense_embedding_service.embed_query(query)

        sparse_vector = self.sparse_embedding_service.embed_query(query)

        return self.vector_store.hybrid_search(
            dense_query_vector=dense_vector,
            sparse_query_vector=sparse_vector,
            limit=limit,
        )

    # =========================================================
    # VALIDATION
    # =========================================================

    @staticmethod
    def _validate_query(query: str) -> None:

        if not query or not query.strip():
            raise ValueError("Query must not be empty.")

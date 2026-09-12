from typing import List

from qdrant_client import QdrantClient, models
from qdrant_client.models import (
    Distance,
    Fusion,
    PointStruct,
    SparseVectorParams,
    VectorParams,
)

from app.config.settings import HybridSearchConfig
from app.models.child_chunk import ChildChunk


class HybridQdrantStore:
    """
    Qdrant storage for hybrid retrieval.

    Every ChildChunk is represented by:

        dense vector
        +
        sparse BM25 vector

    Both representations live on the SAME Qdrant point.
    """

    def __init__(
        self,
        config: HybridSearchConfig,
        vector_size: int,
        url: str = "http://localhost:6333",
    ):
        self.config = config
        self.vector_size = vector_size

        self.client = QdrantClient(
            url=url,
        )

    # =========================================================
    # COLLECTION MANAGEMENT
    # =========================================================

    def recreate_collection(self) -> None:

        collection_name = self.config.collection_name

        if self.client.collection_exists(collection_name):
            print(f"Deleting existing collection: " f"{collection_name}")

            self.client.delete_collection(collection_name=collection_name)

        print(f"Creating hybrid collection: " f"{collection_name}")

        self.client.create_collection(
            collection_name=collection_name,
            # ---------------------------------------------
            # DENSE VECTOR
            # ---------------------------------------------
            vectors_config={
                self.config.dense_vector_name: VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            },
            # ---------------------------------------------
            # SPARSE VECTOR
            # ---------------------------------------------
            sparse_vectors_config={
                self.config.sparse_vector_name: SparseVectorParams(
                    modifier=models.Modifier.IDF,
                ),
            },
        )

    # =========================================================
    # INSERT CHILDREN
    # =========================================================

    def insert_children(
        self,
        children: List[ChildChunk],
        dense_embeddings: List[List[float]],
        sparse_embeddings: List[models.SparseVector],
    ) -> None:

        if not (len(children) == len(dense_embeddings) == len(sparse_embeddings)):
            raise ValueError(
                "children, dense_embeddings and "
                "sparse_embeddings must have equal length."
            )

        points: List[PointStruct] = []

        for child, dense_vector, sparse_vector in zip(
            children, dense_embeddings, sparse_embeddings
        ):

            payload = child.model_dump(mode="json")

            points.append(
                PointStruct(
                    id=str(child.child_id),
                    vector={
                        self.config.dense_vector_name: dense_vector,
                        self.config.sparse_vector_name: sparse_vector,
                    },
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=(self.config.collection_name),
            points=points,
            wait=True,
        )

        print(f"Inserted {len(points)} hybrid child points.")

    # =========================================================
    # DENSE SEARCH
    # =========================================================

    def dense_search(self, query_vector: List[float], limit: int = 10):

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            query=query_vector,
            using=(self.config.dense_vector_name),
            limit=limit,
            with_payload=True,
        )

        return response.points

    # =========================================================
    # SPARSE SEARCH
    # =========================================================

    def sparse_search(self, query_vector: models.SparseVector, limit: int = 10):

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            query=query_vector,
            using=(self.config.sparse_vector_name),
            limit=limit,
            with_payload=True,
        )

        return response.points

    # =========================================================
    # HYBRID SEARCH
    # =========================================================

    def hybrid_search(
        self,
        dense_query_vector: List[float],
        sparse_query_vector: models.SparseVector,
        limit: int | None = None,
    ):

        final_limit = limit if limit is not None else self.config.final_k

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            # -------------------------------------------------
            # STAGE 1:
            # independently create candidate rankings
            # -------------------------------------------------
            prefetch=[
                models.Prefetch(
                    query=dense_query_vector,
                    using=(self.config.dense_vector_name),
                    limit=(self.config.dense_prefetch_k),
                ),
                models.Prefetch(
                    query=sparse_query_vector,
                    using=(self.config.sparse_vector_name),
                    limit=(self.config.sparse_prefetch_k),
                ),
            ],
            # -------------------------------------------------
            # STAGE 2:
            # combine those rankings using RRF
            # -------------------------------------------------
            query=models.RrfQuery(
                rrf=models.Rrf(
                    k=self.config.rrf_k,
                )
            ),
            limit=final_limit,
            with_payload=True,
        )

        return response.points

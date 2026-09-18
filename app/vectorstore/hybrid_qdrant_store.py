import logging
from typing import List

from qdrant_client import QdrantClient, models

from qdrant_client.models import (
    Distance,
    PointStruct,
    SparseVectorParams,
    VectorParams,
)

from app.config.settings import HybridSearchConfig
from app.models.child_chunk import ChildChunk

logger = logging.getLogger(__name__)


class HybridQdrantStore:
    """
    Qdrant storage for hybrid retrieval.

    Every ChildChunk is represented by:

        one Qdrant point
            ├── dense vector
            ├── sparse BM25 vector
            └── search-oriented payload

    The domain model remains normalized.

    The Qdrant payload is intentionally denormalized where
    useful for filtering and diagnostics.
    """

    def __init__(
        self,
        config: HybridSearchConfig,
        vector_size: int,
        url: str = "http://localhost:6333",
    ) -> None:

        self.config = config
        self.vector_size = vector_size
        self.client = QdrantClient(
            url=url,
        )

    # ========================================================
    # COLLECTION MANAGEMENT
    # ========================================================

    def recreate_collection(
        self,
    ) -> None:

        collection_name = self.config.collection_name

        if self.client.collection_exists(collection_name):

            logger.info(
                "Deleting existing Qdrant collection=%s",
                collection_name,
            )

            self.client.delete_collection(collection_name=(collection_name))

        logger.info(
            "Creating Qdrant hybrid collection=%s",
            collection_name,
        )

        self.client.create_collection(
            collection_name=(collection_name),
            vectors_config={
                self.config.dense_vector_name: VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                self.config.sparse_vector_name: SparseVectorParams(
                    modifier=(models.Modifier.IDF),
                ),
            },
        )

        self._create_payload_indexes()

    # ========================================================
    # PAYLOAD INDEXES
    # ========================================================

    def _create_payload_indexes(
        self,
    ) -> None:

        keyword_fields = [
            "document_id",
            "parent_id",
            "parent_key",
            "child_id",
            "child_key",
            "source",
            "content_type",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "section_path",
        ]

        for field_name in keyword_fields:

            self.client.create_payload_index(
                collection_name=(self.config.collection_name),
                field_name=field_name,
                field_schema=(models.PayloadSchemaType.KEYWORD),
            )

        logger.info(
            "Created Qdrant payload indexes collection=%s fields=%d",
            self.config.collection_name,
            len(keyword_fields),
        )

    # ========================================================
    # PAYLOAD PROJECTION
    # ========================================================

    @staticmethod
    def _build_payload(
        child: ChildChunk,
    ) -> dict:
        """
        Build the Qdrant search projection.

        Heading hierarchy is canonical in:

            child.heading_context

        We intentionally flatten it here because Qdrant
        filtering should not need to understand our domain
        object hierarchy.
        """

        heading = child.heading_context

        payload = child.model_dump(
            mode="json",
            exclude={
                "heading_context",
            },
        )

        payload.update(
            {
                "h1": heading.h1,
                "h2": heading.h2,
                "h3": heading.h3,
                "h4": heading.h4,
                "h5": heading.h5,
                "h6": heading.h6,
                "section_path": (heading.get_section_path()),
            }
        )

        return payload

    # ========================================================
    # INSERT CHILDREN
    # ========================================================

    def insert_children(
        self,
        children: List[ChildChunk],
        dense_embeddings: List[List[float]],
        sparse_embeddings: List[models.SparseVector],
    ) -> None:

        if not (len(children) == len(dense_embeddings) == len(sparse_embeddings)):

            raise ValueError(
                "children, dense_embeddings and "
                "sparse_embeddings must have "
                "equal length."
            )

        if not children:
            logger.info("No children supplied for Qdrant insertion.")
            return

        self._validate_unique_child_keys(children)

        points: List[PointStruct] = []

        for (
            child,
            dense_vector,
            sparse_vector,
        ) in zip(
            children,
            dense_embeddings,
            sparse_embeddings,
        ):

            payload = self._build_payload(child)

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

        logger.info(
            "Inserted %d hybrid child points into collection=%s",
            len(points),
            self.config.collection_name,
        )

    # ========================================================
    # DELETE CHILDREN BY DOCUMENT
    # ========================================================

    def delete_by_document_id(
        self,
        document_id: str,
    ) -> None:

        self.client.delete(
            collection_name=(self.config.collection_name),
            points_selector=(
                models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="document_id",
                                match=(models.MatchValue(value=(document_id))),
                            )
                        ]
                    )
                )
            ),
            wait=True,
        )

        logger.info(
            "Deleted Qdrant children for document_id=%s",
            document_id,
        )

    # ========================================================
    # DENSE SEARCH
    # ========================================================

    def dense_search(
        self,
        query_vector: List[float],
        limit: int = 10,
    ):

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            query=query_vector,
            using=(self.config.dense_vector_name),
            limit=limit,
            with_payload=True,
        )

        return response.points

    # ========================================================
    # SPARSE SEARCH
    # ========================================================

    def sparse_search(
        self,
        query_vector: models.SparseVector,
        limit: int = 10,
    ):

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            query=query_vector,
            using=(self.config.sparse_vector_name),
            limit=limit,
            with_payload=True,
        )

        return response.points

    # ========================================================
    # HYBRID SEARCH
    # ========================================================

    def hybrid_search(
        self,
        dense_query_vector: List[float],
        sparse_query_vector: models.SparseVector,
        limit: int | None = None,
    ):

        final_limit = limit if limit is not None else self.config.final_k

        response = self.client.query_points(
            collection_name=(self.config.collection_name),
            prefetch=[
                models.Prefetch(
                    query=(dense_query_vector),
                    using=(self.config.dense_vector_name),
                    limit=(self.config.dense_prefetch_k),
                ),
                models.Prefetch(
                    query=(sparse_query_vector),
                    using=(self.config.sparse_vector_name),
                    limit=(self.config.sparse_prefetch_k),
                ),
            ],
            query=models.RrfQuery(rrf=models.Rrf(k=self.config.rrf_k)),
            limit=final_limit,
            with_payload=True,
        )

        return response.points

    # ========================================================
    # VALIDATION
    # ========================================================

    @staticmethod
    def _validate_unique_child_keys(children: List[ChildChunk]) -> None:

        child_keys = [child.child_key for child in children]
        if len(child_keys) != len(set(child_keys)):

            raise ValueError(
                "Duplicate child_key values " "detected before Qdrant insertion."
            )

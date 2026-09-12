from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)

from app.config.settings import ChunkingConfig
from app.models.child_chunk import ChildChunk

# ============================================================
# QDRANT VECTOR STORE
# ============================================================


class QdrantVectorStore:

    def __init__(
        self,
        config: ChunkingConfig,
        vector_size: int,
    ):

        self.config = config

        self.client = QdrantClient(
            url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
            timeout=60,
        )

        self.vector_size = vector_size

    def recreate_collection(
        self,
    ):

        collections = self.client.get_collections()
        existing = {collection.name for collection in collections.collections}

        if self.config.collection_name in existing:
            print(f"\nDeleting existing collection: " f"{self.config.collection_name}")

            self.client.delete_collection(self.config.collection_name)

        print(f"Creating collection: " f"{self.config.collection_name}")

        self.client.create_collection(
            collection_name=(self.config.collection_name),
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def insert_children(self, chunks: List[ChildChunk], embeddings):
        points = []

        for chunk, vector in zip(chunks, embeddings):

            payload = {
                "document_id": (chunk.document_id),
                "child_id": chunk.child_id,
                "parent_id": chunk.parent_id,
                "source": chunk.source,
                "child_index": (chunk.child_index),
                "content": chunk.content,
                "content_type": (chunk.content_type),
                **chunk.metadata.model_dump(mode="json"),
            }

            points.append(
                PointStruct(
                    id=chunk.child_id,
                    vector=vector.tolist(),
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=(self.config.collection_name),
            points=points,
        )

        print(f"\nInserted {len(points)} " f"children into Qdrant.")

    def search(self, query_vector, top_k: int, with_vectors: bool = False):

        response = self.client.query_points(
            collection_name=self.config.collection_name,
            query=query_vector.tolist(),
            limit=top_k,
            with_payload=True,
            with_vectors=with_vectors,
        )

        return response.points

    def delete_by_document_id(
        self,
        document_id: str,
    ) -> None:

        self.client.delete(
            collection_name=self.config.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(
                                value=document_id,
                            ),
                        )
                    ]
                )
            ),
            wait=True,
        )

    def sync_children(
        self, document_id: str, chunks: List[ChildChunk], embeddings
    ) -> None:

        self.delete_by_document_id(
            document_id=document_id,
        )

        self.insert_children(
            chunks=chunks,
            embeddings=embeddings,
        )

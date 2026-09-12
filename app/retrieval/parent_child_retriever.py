from typing import Dict, List

from pydantic import BaseModel, Field

from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import EmbeddingService
from app.models.parent_chunk import ParentChunk
from app.repositories.parent_repository import ParentRepository
from app.vectorstore.qdrant_store import QdrantVectorStore

# ============================================================
# CHILD SEARCH HIT
# ============================================================


class ChildSearchHit(BaseModel):

    child_id: str

    parent_id: str

    document_id: str

    child_index: int

    content: str

    score: float


# ============================================================
# PARENT RETRIEVAL RESULT
# ============================================================


class ParentRetrievalResult(BaseModel):

    parent: ParentChunk

    best_score: float

    matched_children: List[ChildSearchHit] = Field(default_factory=list)


# ============================================================
# PARENT / CHILD RETRIEVER
# ============================================================


class ParentChildRetriever:

    def __init__(
        self,
        config: ChunkingConfig,
        embedder: EmbeddingService,
        vector_store: QdrantVectorStore,
        parent_repository: ParentRepository,
    ) -> None:

        self.config = config
        self.embedder = embedder
        self.vector_store = vector_store
        self.parent_repository = parent_repository

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        child_top_k: int | None = None,
        child_score_threshold: float | None = None,
        parent_top_k: int | None = None,
    ) -> List[ParentRetrievalResult]:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if child_top_k is None:
            child_top_k = self.config.child_top_k

        if child_top_k <= 0:
            raise ValueError("child_top_k must be greater than zero.")

        if child_score_threshold is None:
            child_score_threshold = self.config.child_score_threshold

        if parent_top_k is None:
            parent_top_k = self.config.parent_top_k

        if (
            child_score_threshold is not None
            and not 0.0 <= child_score_threshold <= 1.0
        ):
            raise ValueError("child_score_threshold must be between " "0.0 and 1.0.")

        if parent_top_k is None:
            parent_top_k = self.config.parent_top_k

        if parent_top_k is not None and parent_top_k <= 0:
            raise ValueError("parent_top_k must be greater than zero.")

        # ----------------------------------------------------
        # 1. QUERY EMBEDDING
        # ----------------------------------------------------

        query_vector = self.embedder.embed_query(query)

        # ----------------------------------------------------
        # 2. CHILD CANDIDATE RETRIEVAL
        # ----------------------------------------------------

        qdrant_hits = self.vector_store.search(
            query_vector=query_vector,
            top_k=child_top_k,
        )

        # ----------------------------------------------------
        # 3. SCORE THRESHOLD + GROUP BY PARENT
        # ----------------------------------------------------

        children_by_parent: Dict[
            str,
            List[ChildSearchHit],
        ] = {}

        for hit in qdrant_hits:

            score = float(hit.score)

            # --------------------------------------------
            # Discard weak semantic matches.
            # --------------------------------------------

            if child_score_threshold is not None and score < child_score_threshold:
                continue

            payload = hit.payload or {}

            parent_id = payload.get("parent_id")

            if not parent_id:
                raise RuntimeError(
                    "Qdrant child payload is missing "
                    "'parent_id'. "
                    f"Point ID: {hit.id}"
                )

            child_hit = ChildSearchHit(
                child_id=payload.get(
                    "child_id",
                    str(hit.id),
                ),
                parent_id=parent_id,
                document_id=payload.get(
                    "document_id",
                    "",
                ),
                child_index=payload.get(
                    "child_index",
                    -1,
                ),
                content=payload.get(
                    "content",
                    "",
                ),
                score=score,
            )

            children_by_parent.setdefault(
                parent_id,
                [],
            ).append(child_hit)

        # ----------------------------------------------------
        # 4. FETCH UNIQUE PARENTS
        # ----------------------------------------------------

        parent_results: List[ParentRetrievalResult] = []

        for (
            parent_id,
            child_hits,
        ) in children_by_parent.items():

            parent = self.parent_repository.get_by_id(parent_id)

            if parent is None:
                raise RuntimeError(
                    "Dangling ChildChunk reference detected. "
                    f"Qdrant child references parent_id="
                    f"{parent_id}, but that ParentChunk "
                    "does not exist in MongoDB."
                )

            # --------------------------------------------
            # Highest-scoring child first.
            # --------------------------------------------

            child_hits.sort(
                key=lambda child: child.score,
                reverse=True,
            )

            parent_results.append(
                ParentRetrievalResult(
                    parent=parent,
                    best_score=child_hits[0].score,
                    matched_children=child_hits,
                )
            )

        # ----------------------------------------------------
        # 5. RANK PARENTS
        # ----------------------------------------------------

        parent_results.sort(
            key=lambda result: result.best_score,
            reverse=True,
        )

        # ----------------------------------------------------
        # 6. FINAL PARENT LIMIT
        # ----------------------------------------------------

        if parent_top_k is not None:
            parent_results = parent_results[:parent_top_k]

        return parent_results

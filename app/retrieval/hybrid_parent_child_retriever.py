from typing import Dict, List

from app.models.parent_chunk import ParentChunk
from app.repositories.parent_repository import ParentRepository

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

from app.retrieval.parent_child_retriever import (
    ChildSearchHit,
    ParentRetrievalResult,
)


class HybridParentChildRetriever:
    """
    Hybrid child retrieval followed by ParentChunk expansion.

    Flow
    ----
    Query
        -> dense + sparse child retrieval
        -> RRF fusion in Qdrant
        -> group children by parent_id
        -> fetch unique parents from MongoDB
        -> return ParentRetrievalResult objects

    The returned type intentionally matches ParentChildRetriever
    so existing CrossEncoder reranking can be reused unchanged.
    """

    def __init__(
        self,
        hybrid_child_retriever: HybridChildRetriever,
        parent_repository: ParentRepository,
    ) -> None:

        self.hybrid_child_retriever = hybrid_child_retriever

        self.parent_repository = parent_repository

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        child_top_k: int = 15,
        parent_top_k: int | None = None,
    ) -> List[ParentRetrievalResult]:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if child_top_k <= 0:
            raise ValueError("child_top_k must be greater than zero.")

        if parent_top_k is not None and parent_top_k <= 0:
            raise ValueError("parent_top_k must be greater than zero.")

        # ====================================================
        # 1. HYBRID CHILD RETRIEVAL
        # ====================================================

        hybrid_hits = self.hybrid_child_retriever.retrieve_hybrid(
            query=query,
            limit=child_top_k,
        )

        if not hybrid_hits:
            return []

        # ====================================================
        # 2. GROUP CHILDREN BY PARENT
        # ====================================================

        children_by_parent: Dict[
            str,
            List[ChildSearchHit],
        ] = {}

        for hit in hybrid_hits:

            payload = hit.payload or {}

            parent_id = payload.get("parent_id")

            if not parent_id:
                raise RuntimeError(
                    "Hybrid Qdrant child payload is "
                    "missing 'parent_id'. "
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
                # IMPORTANT:
                # This is now an RRF fusion score,
                # NOT cosine similarity.
                score=float(hit.score),
            )

            children_by_parent.setdefault(
                parent_id,
                [],
            ).append(child_hit)

        # ====================================================
        # 3. FETCH UNIQUE PARENTS
        # ====================================================

        parent_results: List[ParentRetrievalResult] = []

        for (
            parent_id,
            child_hits,
        ) in children_by_parent.items():

            parent = self.parent_repository.get_by_id(parent_id)

            if parent is None:
                raise RuntimeError(
                    "Dangling ChildChunk reference "
                    "detected. "
                    f"Hybrid child references "
                    f"parent_id={parent_id}, "
                    "but that ParentChunk does not "
                    "exist in MongoDB."
                )

            # -----------------------------------------------
            # Highest RRF child score first.
            # -----------------------------------------------

            child_hits.sort(
                key=lambda child: child.score,
                reverse=True,
            )

            parent_results.append(
                ParentRetrievalResult(
                    parent=parent,
                    # Here best_score means:
                    #
                    # best HYBRID child fusion score,
                    # not dense cosine similarity.
                    best_score=(child_hits[0].score),
                    matched_children=child_hits,
                )
            )

        # ====================================================
        # 4. ORDER PARENTS BY BEST HYBRID CHILD
        # ====================================================

        parent_results.sort(
            key=lambda result: result.best_score,
            reverse=True,
        )

        # ====================================================
        # 5. OPTIONAL PARENT LIMIT
        # ====================================================

        if parent_top_k is not None:

            parent_results = parent_results[:parent_top_k]

        return parent_results

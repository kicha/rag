from typing import List

import torch
from pydantic import BaseModel, Field
from sentence_transformers import CrossEncoder

from app.retrieval.parent_child_retriever import (
    ParentRetrievalResult,
)

# ============================================================
# RERANKED RESULT
# ============================================================


class RerankedParentResult(BaseModel):
    original_rank: int
    reranked_rank: int
    vector_score: float
    reranker_score: float
    result: ParentRetrievalResult


# ============================================================
# RERANKING RESPONSE
# ============================================================


class RerankingResponse(BaseModel):

    query: str
    candidate_count: int
    returned_count: int
    results: List[RerankedParentResult] = Field(default_factory=list)


# ============================================================
# CROSS-ENCODER RERANKER
# ============================================================


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = ("cross-encoder/" "ms-marco-MiniLM-L6-v2"),
    ) -> None:

        self.model_name = model_name

        print(f"Loading reranker model: " f"{self.model_name}")

        # ----------------------------------------------------
        # MS MARCO CrossEncoder models normally return logits.
        #
        # Sigmoid converts those logits to a convenient
        # 0..1 relevance score.
        #
        # This does NOT change ranking order.
        # ----------------------------------------------------

        self.model = CrossEncoder(
            self.model_name,
            activation_fn=torch.nn.Sigmoid(),
        )

    # ========================================================
    # RERANK
    # ========================================================

    def rerank(
        self,
        query: str,
        candidates: List[ParentRetrievalResult],
        top_k: int | None = None,
    ) -> RerankingResponse:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if top_k is not None and top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not candidates:

            return RerankingResponse(
                query=query,
                candidate_count=0,
                returned_count=0,
                results=[],
            )

        # ----------------------------------------------------
        # Build:
        #
        # [
        #   (query, parent_1_content),
        #   (query, parent_2_content),
        #   ...
        # ]
        #
        # The CrossEncoder sees query + document TOGETHER.
        # ----------------------------------------------------

        pairs = [
            (
                query,
                candidate.parent.content,
            )
            for candidate in candidates
        ]

        # ----------------------------------------------------
        # CROSS-ENCODER INFERENCE
        # ----------------------------------------------------

        scores = self.model.predict(pairs)

        # ----------------------------------------------------
        # Preserve original vector ranking.
        # ----------------------------------------------------

        scored_results = []

        for original_index, (
            candidate,
            reranker_score,
        ) in enumerate(
            zip(
                candidates,
                scores,
            ),
            start=1,
        ):

            scored_results.append(
                {
                    "original_rank": original_index,
                    "vector_score": candidate.best_score,
                    "reranker_score": float(reranker_score),
                    "candidate": candidate,
                }
            )

        # ----------------------------------------------------
        # Sort using CROSS-ENCODER score.
        # ----------------------------------------------------

        scored_results.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        # ----------------------------------------------------
        # Apply final top-k AFTER reranking.
        # ----------------------------------------------------

        if top_k is not None:

            scored_results = scored_results[:top_k]

        # ----------------------------------------------------
        # Convert to typed Pydantic output.
        # ----------------------------------------------------

        reranked_results: List[RerankedParentResult] = []

        for reranked_index, item in enumerate(
            scored_results,
            start=1,
        ):

            reranked_results.append(
                RerankedParentResult(
                    original_rank=(item["original_rank"]),
                    reranked_rank=(reranked_index),
                    vector_score=(item["vector_score"]),
                    reranker_score=(item["reranker_score"]),
                    result=(item["candidate"]),
                )
            )

        return RerankingResponse(
            query=query,
            candidate_count=len(candidates),
            returned_count=len(reranked_results),
            results=reranked_results,
        )

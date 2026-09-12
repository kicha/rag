from typing import List

import numpy as np
from pydantic import BaseModel, Field

# ============================================================
# MMR CANDIDATE
# ============================================================


class MMRCandidate(BaseModel):

    id: str
    content: str
    query_similarity: float
    embedding: List[float]
    metadata: dict = Field(default_factory=dict)


# ============================================================
# MMR RESULT
# ============================================================


class MMRResult(BaseModel):
    rank: int
    id: str
    content: str

    query_similarity: float
    max_redundancy: float

    relevance_contribution: float
    redundancy_penalty: float

    mmr_score: float

    metadata: dict = Field(default_factory=dict)


# ============================================================
# MMR RETRIEVER
# ============================================================


class MMRRetriever:

    def __init__(
        self,
        lambda_mult: float = 0.5,
    ) -> None:

        if not 0.0 <= lambda_mult <= 1.0:
            raise ValueError("lambda_mult must be between 0.0 and 1.0.")

        self.lambda_mult = lambda_mult

    # ========================================================
    # COSINE SIMILARITY
    # ========================================================

    @staticmethod
    def _cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray,
    ) -> float:

        denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)

        if denominator == 0.0:
            return 0.0

        return float(
            np.dot(
                vector_a,
                vector_b,
            )
            / denominator
        )

    # ========================================================
    # SELECT
    # ========================================================

    def select(
        self,
        candidates: List[MMRCandidate],
        top_k: int,
    ) -> List[MMRResult]:

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not candidates:
            return []

        # ----------------------------------------------------
        # Highest query similarity becomes first result.
        # ----------------------------------------------------

        remaining = candidates.copy()

        first = max(
            remaining,
            key=lambda candidate: candidate.query_similarity,
        )

        selected = [first]

        remaining.remove(first)

        results = [
            MMRResult(
                rank=1,
                id=first.id,
                content=first.content,
                query_similarity=first.query_similarity,
                max_redundancy=0.0,
                relevance_contribution=first.query_similarity,
                redundancy_penalty=0.0,
                mmr_score=first.query_similarity,
                metadata=first.metadata,
            )
        ]

        best_candidate = None
        best_mmr_score = float("-inf")
        best_max_redundancy = 0.0
        best_relevance_contribution = 0.0
        best_redundancy_penalty = 0.0
        # ----------------------------------------------------
        # ITERATIVE MMR SELECTION
        # ----------------------------------------------------

        while remaining and len(selected) < top_k:

            best_candidate = None
            best_mmr_score = float("-inf")

            for candidate in remaining:
                candidate_vector = np.array(
                    candidate.embedding,
                    dtype=np.float32,
                )

                # --------------------------------------------
                # Find maximum similarity between this
                # candidate and anything already selected.
                # --------------------------------------------

                max_selected_similarity = float("-inf")

                for selected_candidate in selected:
                    selected_vector = np.array(
                        selected_candidate.embedding,
                        dtype=np.float32,
                    )

                    similarity = self._cosine_similarity(
                        candidate_vector,
                        selected_vector,
                    )

                    max_selected_similarity = max(
                        max_selected_similarity,
                        similarity,
                    )

                # --------------------------------------------
                # MMR
                # --------------------------------------------

                # mmr_score = (
                #     self.lambda_mult * candidate.query_similarity
                #     - (1.0 - self.lambda_mult) * max_selected_similarity
                # )
                relevance_contribution = self.lambda_mult * candidate.query_similarity

                redundancy_penalty = (1.0 - self.lambda_mult) * max_selected_similarity

                mmr_score = relevance_contribution - redundancy_penalty

                if mmr_score > best_mmr_score:

                    best_candidate = candidate
                    best_mmr_score = mmr_score

                    best_max_redundancy = max_selected_similarity
                    best_relevance_contribution = relevance_contribution
                    best_redundancy_penalty = redundancy_penalty

            if best_candidate is None:
                break

            selected.append(best_candidate)
            remaining.remove(best_candidate)

            results.append(
                MMRResult(
                    rank=len(results) + 1,
                    id=best_candidate.id,
                    content=best_candidate.content,
                    query_similarity=best_candidate.query_similarity,
                    max_redundancy=best_max_redundancy,
                    relevance_contribution=best_relevance_contribution,
                    redundancy_penalty=best_redundancy_penalty,
                    mmr_score=best_mmr_score,
                    metadata=best_candidate.metadata,
                )
            )

        return results

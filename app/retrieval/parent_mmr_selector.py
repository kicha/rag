from typing import List
import numpy as np
from pydantic import BaseModel

from app.models.parent_chunk import ParentChunk

# ============================================================
# INPUT CANDIDATE
# ============================================================


# class ParentMMRCandidate(BaseModel):
#     parent: ParentChunk
#     # Relevance supplied by the CrossEncoder.
#     relevance_score: float

#     # Dense embedding of the complete ParentChunk.
#     embedding: List[float]

#     # Original CrossEncoder rank before MMR.
#     reranker_rank: int


class ParentMMRCandidate(BaseModel):
    parent: ParentChunk

    # Dense cosine similarity between:
    # query embedding ↔ parent embedding
    query_similarity: float

    # Used only for traceability.
    cross_encoder_score: float
    cross_encoder_rank: int

    embedding: List[float]


# ============================================================
# OUTPUT RESULT
# ============================================================


# class ParentMMRResult(BaseModel):
#     rank: int
#     parent: ParentChunk
#     reranker_rank: int
#     relevance_score: float
#     max_redundancy: float
#     relevance_contribution: float
#     redundancy_penalty: float
#     mmr_score: float


class ParentMMRResult(BaseModel):
    rank: int
    parent: ParentChunk
    cross_encoder_rank: int
    cross_encoder_score: float
    query_similarity: float
    max_redundancy: float
    relevance_contribution: float
    redundancy_penalty: float
    mmr_score: float


# ============================================================
# PARENT-LEVEL MMR
# ============================================================


class ParentMMRSelector:

    def __init__(
        self,
        lambda_mult: float = 0.7,
    ) -> None:

        if not 0.0 <= lambda_mult <= 1.0:
            raise ValueError("lambda_mult must be between 0 and 1.")

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
        candidates: List[ParentMMRCandidate],
        top_k: int,
    ) -> List[ParentMMRResult]:

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not candidates:
            return []

        remaining = candidates.copy()

        # ====================================================
        # FIRST RESULT
        #
        # Highest CrossEncoder relevance wins.
        # No diversity comparison exists yet.
        # ====================================================

        # first = max(
        #     remaining,
        #     key=lambda candidate: candidate.relevance_score,
        # )

        first = max(
            remaining,
            key=lambda candidate: candidate.query_similarity,
        )

        remaining.remove(first)

        selected = [first]

        # results = [
        #     ParentMMRResult(
        #         rank=1,
        #         parent=first.parent,
        #         reranker_rank=first.reranker_rank,
        #         relevance_score=(first.relevance_score),
        #         max_redundancy=0.0,
        #         relevance_contribution=(first.relevance_score),
        #         redundancy_penalty=0.0,
        #         mmr_score=(first.relevance_score),
        #     )
        # ]

        results = [
            ParentMMRResult(
                rank=1,
                parent=first.parent,
                cross_encoder_rank=first.cross_encoder_rank,
                cross_encoder_score=first.cross_encoder_score,
                query_similarity=first.query_similarity,
                max_redundancy=0.0,
                relevance_contribution=first.query_similarity,
                redundancy_penalty=0.0,
                mmr_score=first.query_similarity,
            )
        ]

        # ====================================================
        # SUBSEQUENT RESULTS
        # ====================================================

        while remaining and len(selected) < top_k:

            best_candidate = None
            best_mmr_score = float("-inf")

            best_max_redundancy = 0.0
            best_relevance_contribution = 0.0
            best_redundancy_penalty = 0.0

            for candidate in remaining:

                candidate_vector = np.asarray(
                    candidate.embedding,
                    dtype=np.float32,
                )

                max_redundancy = float("-inf")

                for selected_candidate in selected:

                    selected_vector = np.asarray(
                        selected_candidate.embedding,
                        dtype=np.float32,
                    )

                    similarity = self._cosine_similarity(
                        candidate_vector,
                        selected_vector,
                    )

                    max_redundancy = max(
                        max_redundancy,
                        similarity,
                    )

                # relevance_contribution = self.lambda_mult * candidate.relevance_score
                relevance_contribution = self.lambda_mult * candidate.query_similarity

                redundancy_penalty = (1.0 - self.lambda_mult) * max_redundancy

                mmr_score = relevance_contribution - redundancy_penalty

                if mmr_score > best_mmr_score:

                    best_candidate = candidate
                    best_mmr_score = mmr_score

                    best_max_redundancy = max_redundancy

                    best_relevance_contribution = relevance_contribution

                    best_redundancy_penalty = redundancy_penalty

            if best_candidate is None:
                break

            selected.append(best_candidate)

            remaining.remove(best_candidate)

            # results.append(
            #     ParentMMRResult(
            #         rank=len(results) + 1,
            #         parent=best_candidate.parent,
            #         reranker_rank=(best_candidate.reranker_rank),
            #         relevance_score=(best_candidate.relevance_score),
            #         max_redundancy=(best_max_redundancy),
            #         relevance_contribution=(best_relevance_contribution),
            #         redundancy_penalty=(best_redundancy_penalty),
            #         mmr_score=(best_mmr_score),
            #     )
            # )

            results.append(
                ParentMMRResult(
                    rank=len(results) + 1,
                    parent=best_candidate.parent,
                    cross_encoder_rank=(best_candidate.cross_encoder_rank),
                    cross_encoder_score=(best_candidate.cross_encoder_score),
                    query_similarity=(best_candidate.query_similarity),
                    max_redundancy=(best_max_redundancy),
                    relevance_contribution=(best_relevance_contribution),
                    redundancy_penalty=(best_redundancy_penalty),
                    mmr_score=best_mmr_score,
                )
            )

        return results

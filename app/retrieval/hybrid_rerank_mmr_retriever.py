from typing import List

import numpy as np

from app.embeddings.embedding_service import (
    EmbeddingService,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.retrieval.hybrid_parent_child_retriever import (
    HybridParentChildRetriever,
)

from app.retrieval.parent_mmr_selector import (
    ParentMMRCandidate,
    ParentMMRResult,
    ParentMMRSelector,
)


class HybridRerankMMRRetriever:
    """
    Full advanced retrieval pipeline.

    Flow
    ----
    Query
        -> Hybrid child retrieval
        -> RRF fusion
        -> Parent expansion/deduplication
        -> CrossEncoder parent reranking
        -> CrossEncoder pruning
        -> Dense parent MMR
        -> final ParentChunks
    """

    def __init__(
        self,
        hybrid_parent_child_retriever: HybridParentChildRetriever,
        reranker: CrossEncoderReranker,
        embedder: EmbeddingService,
        lambda_mult: float = 0.7,
    ) -> None:

        self.hybrid_parent_child_retriever = hybrid_parent_child_retriever

        self.reranker = reranker
        self.embedder = embedder

        self.mmr_selector = ParentMMRSelector(lambda_mult=lambda_mult)

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
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        child_top_k: int = 15,
        cross_encoder_top_k: int = 5,
        final_top_k: int = 3,
    ) -> List[ParentMMRResult]:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if child_top_k <= 0:
            raise ValueError("child_top_k must be " "greater than zero.")

        if cross_encoder_top_k <= 0:
            raise ValueError("cross_encoder_top_k must be " "greater than zero.")

        if final_top_k <= 0:
            raise ValueError("final_top_k must be " "greater than zero.")

        if final_top_k > cross_encoder_top_k:
            raise ValueError("final_top_k cannot exceed " "cross_encoder_top_k.")

        # ====================================================
        # 1. HYBRID CHILD -> PARENT RETRIEVAL
        # ====================================================

        parent_candidates = self.hybrid_parent_child_retriever.retrieve(
            query=query,
            # RRF returns this many children.
            child_top_k=child_top_k,
            # Give CrossEncoder the broadest
            # unique parent candidate pool available.
            parent_top_k=None,
        )

        if not parent_candidates:
            return []

        # ====================================================
        # 2. CROSS-ENCODER PARENT RERANKING
        # ====================================================

        reranked_response = self.reranker.rerank(
            query=query,
            candidates=parent_candidates,
            top_k=cross_encoder_top_k,
        )

        if not reranked_response.results:
            return []

        # ====================================================
        # 3. DENSE QUERY EMBEDDING
        # ====================================================

        query_embedding = np.asarray(
            self.embedder.embed_query(query),
            dtype=np.float32,
        )

        # ====================================================
        # 4. EMBED CROSS-ENCODER SURVIVOR PARENTS
        # ====================================================

        parent_texts = [
            item.result.parent.content for item in reranked_response.results
        ]

        parent_embeddings = self.embedder.embed_documents(parent_texts)

        # ====================================================
        # 5. BUILD PARENT MMR CANDIDATES
        # ====================================================

        mmr_candidates: List[ParentMMRCandidate] = []

        for (
            reranked_item,
            parent_embedding,
        ) in zip(
            reranked_response.results,
            parent_embeddings,
        ):

            parent_vector = np.asarray(
                parent_embedding,
                dtype=np.float32,
            )

            # -----------------------------------------------
            # MMR relevance stays in dense cosine space.
            #
            # IMPORTANT:
            #
            # We do NOT use:
            #   RRF score
            #
            # and we do NOT use:
            #   CrossEncoder score
            #
            # numerically inside MMR.
            # -----------------------------------------------

            query_similarity = self._cosine_similarity(
                query_embedding,
                parent_vector,
            )

            mmr_candidates.append(
                ParentMMRCandidate(
                    parent=(reranked_item.result.parent),
                    query_similarity=(query_similarity),
                    cross_encoder_score=(reranked_item.reranker_score),
                    cross_encoder_rank=(reranked_item.reranked_rank),
                    embedding=(parent_vector.tolist()),
                )
            )

        # ====================================================
        # 6. DENSE PARENT MMR
        # ====================================================

        return self.mmr_selector.select(
            candidates=mmr_candidates,
            top_k=final_top_k,
        )

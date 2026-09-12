from typing import List

import numpy as np

from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)
from app.retrieval.parent_child_retriever import (
    ParentChildRetriever,
)
from app.retrieval.parent_mmr_selector import (
    ParentMMRCandidate,
    ParentMMRResult,
    ParentMMRSelector,
)


class RerankMMRRetriever:

    def __init__(
        self,
        parent_child_retriever: ParentChildRetriever,
        reranker: CrossEncoderReranker,
        embedder: EmbeddingService,
        lambda_mult: float = 0.7,
    ) -> None:

        self.parent_child_retriever = parent_child_retriever

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

        if final_top_k > cross_encoder_top_k:
            raise ValueError("final_top_k cannot exceed " "cross_encoder_top_k.")

        # ====================================================
        # 1. BROAD VECTOR RETRIEVAL
        # ====================================================

        parent_candidates = self.parent_child_retriever.retrieve(
            query=query,
            child_top_k=child_top_k,
            child_score_threshold=0.0,
            # Important:
            # give the CrossEncoder a broad parent pool.
            parent_top_k=child_top_k,
        )

        if not parent_candidates:
            return []

        # ====================================================
        # 2. CROSS-ENCODER RELEVANCE RANKING
        #
        # CrossEncoder decides which parents are worth
        # continuing with.
        # ====================================================

        reranked_response = self.reranker.rerank(
            query=query,
            candidates=parent_candidates,
            top_k=cross_encoder_top_k,
        )

        if not reranked_response.results:
            return []

        # ====================================================
        # 3. EMBED QUERY
        # ====================================================

        query_embedding = np.asarray(
            self.embedder.embed_query(query),
            dtype=np.float32,
        )

        # ====================================================
        # 4. EMBED ONLY CROSS-ENCODER SURVIVORS
        # ====================================================

        parent_texts = [
            item.result.parent.content for item in reranked_response.results
        ]

        parent_embeddings = self.embedder.embed_documents(parent_texts)

        # ====================================================
        # 5. BUILD MMR CANDIDATES
        #
        # MMR relevance:
        # query embedding ↔ parent embedding
        #
        # MMR redundancy:
        # parent embedding ↔ selected parent embeddings
        #
        # CrossEncoder scores are stored only as metadata.
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
        # 6. FINAL DIVERSITY SELECTION
        # ====================================================

        return self.mmr_selector.select(
            candidates=mmr_candidates,
            top_k=final_top_k,
        )

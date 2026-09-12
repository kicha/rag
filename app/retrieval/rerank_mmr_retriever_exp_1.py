from typing import List

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
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        child_top_k: int = 15,
        reranker_candidate_top_k: int = 6,
        final_top_k: int = 3,
    ) -> List[ParentMMRResult]:

        # ====================================================
        # 1. BROAD VECTOR RETRIEVAL + PARENT EXPANSION
        # ====================================================

        parent_candidates = self.parent_child_retriever.retrieve(
            query=query,
            child_top_k=child_top_k,
            child_score_threshold=0.0,
            parent_top_k=(reranker_candidate_top_k),
        )

        if not parent_candidates:
            return []

        # ====================================================
        # 2. CROSS-ENCODER RELEVANCE RERANKING
        #
        # IMPORTANT:
        # We keep several candidates here.
        # MMR will perform the final selection.
        # ====================================================

        reranked_response = self.reranker.rerank(
            query=query,
            candidates=parent_candidates,
            top_k=(reranker_candidate_top_k),
        )

        # ====================================================
        # 3. EMBED PARENTS FOR DIVERSITY COMPARISON
        #
        # CrossEncoder score measures query relevance.
        #
        # Dense embeddings measure similarity between
        # ParentChunks for the MMR redundancy term.
        # ====================================================

        parent_texts = [
            item.result.parent.content for item in reranked_response.results
        ]

        parent_embeddings = self.embedder.embed_documents(parent_texts)

        # ====================================================
        # 4. BUILD PARENT-MMR CANDIDATES
        # ====================================================

        mmr_candidates: List[ParentMMRCandidate] = []

        for (
            reranked_item,
            embedding,
        ) in zip(
            reranked_response.results,
            parent_embeddings,
        ):

            mmr_candidates.append(
                ParentMMRCandidate(
                    parent=(reranked_item.result.parent),
                    relevance_score=(reranked_item.reranker_score),
                    embedding=(
                        embedding.tolist()
                        if hasattr(
                            embedding,
                            "tolist",
                        )
                        else list(embedding)
                    ),
                    reranker_rank=(reranked_item.reranked_rank),
                )
            )

        # ====================================================
        # 5. FINAL PARENT-LEVEL MMR
        # ====================================================

        return self.mmr_selector.select(
            candidates=mmr_candidates,
            top_k=final_top_k,
        )

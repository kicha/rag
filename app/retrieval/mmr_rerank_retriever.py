from typing import List

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
    RerankingResponse,
)
from app.retrieval.mmr_parent_child_retriever import MMRParentChildRetriever
from app.retrieval.parent_child_retriever import ParentRetrievalResult


class MMRRerankRetriever:

    def __init__(
        self,
        mmr_retriever: MMRParentChildRetriever,
        reranker: CrossEncoderReranker,
    ) -> None:

        self.mmr_retriever = mmr_retriever
        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        fetch_k: int = 10,
        mmr_child_top_k: int = 5,
        mmr_parent_top_k: int = 5,
        reranker_top_k: int = 3,
    ) -> RerankingResponse:

        # ----------------------------------------------------
        # 1. MMR candidate selection
        # ----------------------------------------------------

        mmr_parent_results = self.mmr_retriever.retrieve(
            query=query,
            fetch_k=fetch_k,
            mmr_child_top_k=mmr_child_top_k,
            parent_top_k=mmr_parent_top_k,
        )

        wide_mmr_results = self.mmr_retriever.retrieve(
            query=query,
            fetch_k=15,
            mmr_child_top_k=8,
            parent_top_k=6,
        )

        print(f"\nMMR unique parents sent to reranker: " f"{len(wide_mmr_results)}")
        # ----------------------------------------------------
        # 2. Adapt MMR parent results into the existing
        #    ParentRetrievalResult model expected by
        #    CrossEncoderReranker.
        # ----------------------------------------------------

        rerank_candidates: List[ParentRetrievalResult] = []

        for mmr_result in mmr_parent_results:

            rerank_candidates.append(
                ParentRetrievalResult(
                    parent=mmr_result.parent,
                    # We use the best original query
                    # similarity among the MMR-selected
                    # children as the vector-stage score.
                    best_score=(mmr_result.best_query_similarity),
                    # CrossEncoderReranker does not require
                    # these child details to score the parent,
                    # so this can remain empty here.
                    matched_children=[],
                )
            )

        # ----------------------------------------------------
        # 3. CrossEncoder reranking
        # ----------------------------------------------------

        return self.reranker.rerank(
            query=query,
            candidates=rerank_candidates,
            top_k=reranker_top_k,
        )

from __future__ import annotations

from typing import List

from pydantic import BaseModel

from app.querying.query_rewriter import (
    QueryRewriteResult,
    QueryRewriter,
)

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

from app.retrieval.parent_mmr_selector import (
    ParentMMRResult,
)

# ============================================================
# RESULT
# ============================================================


class RewrittenQueryRetrievalResult(BaseModel):
    rewrite: QueryRewriteResult

    results: List[ParentMMRResult]


# ============================================================
# RETRIEVER
# ============================================================


class RewrittenQueryRetriever:

    def __init__(
        self,
        query_rewriter: QueryRewriter,
        retriever: HybridRerankMMRRetriever,
    ) -> None:

        self.query_rewriter = query_rewriter

        self.retriever = retriever

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        context: str | None = None,
        child_top_k: int = 30,
        cross_encoder_top_k: int = 10,
        final_top_k: int = 3,
    ) -> RewrittenQueryRetrievalResult:

        # ====================================================
        # 1. QUERY TRANSFORMATION
        # ====================================================

        rewrite_result = self.query_rewriter.rewrite(
            query=query,
            context=context,
        )

        # ====================================================
        # 2. EXISTING RETRIEVAL FUNNEL
        #
        # IMPORTANT:
        # Every downstream stage sees the SAME rewritten query:
        #
        # - dense embedding
        # - sparse embedding
        # - CrossEncoder
        # - dense MMR query similarity
        # ====================================================

        results = self.retriever.retrieve(
            query=(rewrite_result.rewritten_query),
            child_top_k=(child_top_k),
            cross_encoder_top_k=(cross_encoder_top_k),
            final_top_k=(final_top_k),
        )

        return RewrittenQueryRetrievalResult(
            rewrite=rewrite_result,
            results=results,
        )

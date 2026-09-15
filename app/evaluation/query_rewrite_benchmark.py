from __future__ import annotations

from time import perf_counter
from typing import List, Literal

from pydantic import BaseModel

from app.evaluation.retrieval_benchmark import (
    GoldQuery,
)
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
# TYPES
# ============================================================

RewriteOutcome = Literal[
    "WIN",
    "TIE",
    "LOSS",
]


# ============================================================
# RETRIEVAL SNAPSHOT
# ============================================================


class RetrievalSnapshot(BaseModel):
    query_used: str

    retrieved_documents: List[str]

    hit_at_3: float
    recall_at_3: float
    precision_at_3: float
    reciprocal_rank: float

    first_relevant_rank: int | None

    retrieval_latency_ms: float


# ============================================================
# PER-QUERY COMPARISON
# ============================================================


class QueryRewriteComparison(BaseModel):
    original_query: str
    rewritten_query: str

    query_class: str

    relevant_docs: List[str]

    rewrite_changed: bool
    rewrite_reason: str
    rewrite_latency_ms: float

    rewrite_used_fallback: bool

    original: RetrievalSnapshot
    rewritten: RetrievalSnapshot

    outcome: RewriteOutcome

    recall_delta: float
    precision_delta: float
    reciprocal_rank_delta: float

    rewritten_total_latency_ms: float


# ============================================================
# SUMMARY
# ============================================================


class QueryRewriteBenchmarkSummary(BaseModel):
    evaluated_queries: int

    rewrites_changed: int
    rewrites_unchanged: int
    rewrite_fallbacks: int

    wins: int
    ties: int
    losses: int

    win_rate: float
    loss_rate: float

    original_hit_at_3: float
    rewritten_hit_at_3: float

    original_recall_at_3: float
    rewritten_recall_at_3: float

    original_precision_at_3: float
    rewritten_precision_at_3: float

    original_mrr: float
    rewritten_mrr: float

    average_rewrite_latency_ms: float

    average_original_retrieval_ms: float
    average_rewritten_retrieval_ms: float

    average_rewritten_total_ms: float


# ============================================================
# FULL REPORT
# ============================================================


class QueryRewriteBenchmarkReport(BaseModel):
    comparisons: List[QueryRewriteComparison]

    summary: QueryRewriteBenchmarkSummary


# ============================================================
# EVALUATOR
# ============================================================


class QueryRewriteBenchmarkEvaluator:

    def __init__(
        self,
        query_rewriter: QueryRewriter,
        retriever: HybridRerankMMRRetriever,
        child_top_k: int = 30,
        cross_encoder_top_k: int = 10,
        final_top_k: int = 3,
    ) -> None:

        if child_top_k <= 0:
            raise ValueError("child_top_k must be greater than zero.")

        if cross_encoder_top_k <= 0:
            raise ValueError("cross_encoder_top_k must be " "greater than zero.")

        if final_top_k <= 0:
            raise ValueError("final_top_k must be greater than zero.")

        if final_top_k > cross_encoder_top_k:
            raise ValueError("final_top_k cannot exceed " "cross_encoder_top_k.")

        self.query_rewriter = query_rewriter

        self.retriever = retriever

        self.child_top_k = child_top_k

        self.cross_encoder_top_k = cross_encoder_top_k

        self.final_top_k = final_top_k

    # ========================================================
    # METRICS
    # ========================================================

    @staticmethod
    def _first_relevant_rank(
        retrieved_docs: List[str],
        relevant_docs: set[str],
    ) -> int | None:

        for rank, document_id in enumerate(
            retrieved_docs,
            start=1,
        ):

            if document_id in relevant_docs:
                return rank

        return None

    # --------------------------------------------------------

    @staticmethod
    def _hit_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        return 1.0 if set(retrieved_docs[:k]) & relevant_docs else 0.0

    # --------------------------------------------------------

    @staticmethod
    def _recall_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        if not relevant_docs:
            return 0.0

        found = set(retrieved_docs[:k]) & relevant_docs

        return len(found) / len(relevant_docs)

    # --------------------------------------------------------

    @staticmethod
    def _precision_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        top_k = retrieved_docs[:k]

        if not top_k:
            return 0.0

        relevant_count = sum(1 for document_id in top_k if document_id in relevant_docs)

        return relevant_count / len(top_k)

    # --------------------------------------------------------

    @staticmethod
    def _reciprocal_rank(
        first_relevant_rank: int | None,
    ) -> float:

        if first_relevant_rank is None:
            return 0.0

        return 1.0 / first_relevant_rank

    # ========================================================
    # RUN RETRIEVAL
    # ========================================================

    def _run_retrieval(
        self,
        query: str,
        relevant_docs: List[str],
    ) -> RetrievalSnapshot:

        started = perf_counter()

        results: List[ParentMMRResult] = self.retriever.retrieve(
            query=query,
            child_top_k=(self.child_top_k),
            cross_encoder_top_k=(self.cross_encoder_top_k),
            final_top_k=(self.final_top_k),
        )

        latency_ms = (perf_counter() - started) * 1000.0

        retrieved_docs = [result.parent.document_id for result in results]

        relevant_set = set(relevant_docs)

        first_rank = self._first_relevant_rank(
            retrieved_docs=(retrieved_docs),
            relevant_docs=(relevant_set),
        )

        return RetrievalSnapshot(
            query_used=query,
            retrieved_documents=(retrieved_docs),
            hit_at_3=(
                self._hit_at_k(
                    retrieved_docs,
                    relevant_set,
                    3,
                )
            ),
            recall_at_3=(
                self._recall_at_k(
                    retrieved_docs,
                    relevant_set,
                    3,
                )
            ),
            precision_at_3=(
                self._precision_at_k(
                    retrieved_docs,
                    relevant_set,
                    3,
                )
            ),
            reciprocal_rank=(self._reciprocal_rank(first_rank)),
            first_relevant_rank=(first_rank),
            retrieval_latency_ms=(latency_ms),
        )

    # ========================================================
    # WIN / TIE / LOSS
    # ========================================================

    @staticmethod
    def _compare_first_relevant_rank(
        original_rank: int | None,
        rewritten_rank: int | None,
    ) -> RewriteOutcome:

        # ----------------------------------------------------
        # Original failed, rewrite succeeded.
        # ----------------------------------------------------

        if original_rank is None and rewritten_rank is not None:
            return "WIN"

        # ----------------------------------------------------
        # Original succeeded, rewrite lost the evidence.
        # ----------------------------------------------------

        if original_rank is not None and rewritten_rank is None:
            return "LOSS"

        # ----------------------------------------------------
        # Neither found relevant evidence.
        # ----------------------------------------------------

        if original_rank is None and rewritten_rank is None:
            return "TIE"

        # ----------------------------------------------------
        # Both succeeded:
        # smaller rank is better.
        # ----------------------------------------------------

        assert original_rank is not None
        assert rewritten_rank is not None

        if rewritten_rank < original_rank:
            return "WIN"

        if rewritten_rank > original_rank:
            return "LOSS"

        return "TIE"

    # ========================================================
    # ONE QUERY
    # ========================================================

    def evaluate_query(
        self,
        gold: GoldQuery,
    ) -> QueryRewriteComparison:

        # ====================================================
        # 1. ORIGINAL QUERY PIPELINE
        # ====================================================

        original_snapshot = self._run_retrieval(
            query=gold.query,
            relevant_docs=(gold.relevant_docs),
        )

        # ====================================================
        # 2. QUERY REWRITE
        #
        # IMPORTANT:
        # Do not inject gold labels or relevant documents into
        # the rewriter. That would leak evaluation answers.
        #
        # This benchmark tests standalone rewriting.
        # ====================================================

        rewrite_result: QueryRewriteResult = self.query_rewriter.rewrite(
            query=gold.query,
            context=None,
        )

        # ====================================================
        # 3. REWRITTEN QUERY PIPELINE
        # ====================================================

        rewritten_snapshot = self._run_retrieval(
            query=(rewrite_result.rewritten_query),
            relevant_docs=(gold.relevant_docs),
        )

        # ====================================================
        # 4. WIN / TIE / LOSS
        #
        # Defined ONLY using the rank of the first relevant
        # document, so this outcome has a clear interpretation.
        #
        # Recall and precision changes are reported separately.
        # ====================================================

        outcome = self._compare_first_relevant_rank(
            original_rank=(original_snapshot.first_relevant_rank),
            rewritten_rank=(rewritten_snapshot.first_relevant_rank),
        )

        return QueryRewriteComparison(
            original_query=(gold.query),
            rewritten_query=(rewrite_result.rewritten_query),
            query_class=(gold.query_class),
            relevant_docs=(gold.relevant_docs),
            rewrite_changed=(rewrite_result.changed),
            rewrite_reason=(rewrite_result.reason),
            rewrite_latency_ms=(rewrite_result.latency_ms),
            rewrite_used_fallback=(rewrite_result.used_fallback),
            original=(original_snapshot),
            rewritten=(rewritten_snapshot),
            outcome=(outcome),
            recall_delta=(
                rewritten_snapshot.recall_at_3 - original_snapshot.recall_at_3
            ),
            precision_delta=(
                rewritten_snapshot.precision_at_3 - original_snapshot.precision_at_3
            ),
            reciprocal_rank_delta=(
                rewritten_snapshot.reciprocal_rank - original_snapshot.reciprocal_rank
            ),
            rewritten_total_latency_ms=(
                rewrite_result.latency_ms + rewritten_snapshot.retrieval_latency_ms
            ),
        )

    # ========================================================
    # FULL BENCHMARK
    # ========================================================

    def evaluate(
        self,
        gold_queries: List[GoldQuery],
    ) -> QueryRewriteBenchmarkReport:

        comparisons: List[QueryRewriteComparison] = []

        for index, gold in enumerate(
            gold_queries,
            start=1,
        ):

            # ------------------------------------------------
            # Unanswerable queries need a separate abstention
            # evaluation. Do not mix them into retrieval
            # relevance metrics.
            # ------------------------------------------------

            if not gold.relevant_docs:

                print()
                print(f"[{index:02d}] " f"SKIP UNANSWERABLE: " f"{gold.query}")

                continue

            comparison = self.evaluate_query(gold)

            comparisons.append(comparison)

            self._print_query_result(
                index=index,
                comparison=comparison,
            )

        summary = self._summarize(comparisons)

        return QueryRewriteBenchmarkReport(
            comparisons=comparisons,
            summary=summary,
        )

    # ========================================================
    # PRINT ONE QUERY
    # ========================================================

    @staticmethod
    def _print_query_result(
        index: int,
        comparison: QueryRewriteComparison,
    ) -> None:

        print()
        print("=" * 70)
        print(f"[{index:02d}] " f"{comparison.outcome}")
        print(f"Original   : " f"{comparison.original_query}")
        print(f"Rewritten  : " f"{comparison.rewritten_query}")
        print(f"Relevant   : " f"{comparison.relevant_docs}")
        print(f"Original@3 : " f"{comparison.original.retrieved_documents}")
        print(f"Rewrite@3  : " f"{comparison.rewritten.retrieved_documents}")

        print(
            "Original   : "
            f"RR={comparison.original.reciprocal_rank:.3f}  "
            f"Recall={comparison.original.recall_at_3:.3f}  "
            f"Precision={comparison.original.precision_at_3:.3f}"
        )

        print(
            "Rewritten  : "
            f"RR={comparison.rewritten.reciprocal_rank:.3f}  "
            f"Recall={comparison.rewritten.recall_at_3:.3f}  "
            f"Precision={comparison.rewritten.precision_at_3:.3f}"
        )

        print(f"Rewrite ms : " f"{comparison.rewrite_latency_ms:.2f}")

        print(f"Changed    : " f"{comparison.rewrite_changed}")

        if comparison.rewrite_used_fallback:

            print("WARNING    : " "Rewrite fallback used.")

    # ========================================================
    # SUMMARY
    # ========================================================

    @staticmethod
    def _summarize(
        comparisons: List[QueryRewriteComparison],
    ) -> QueryRewriteBenchmarkSummary:

        count = len(comparisons)

        if count == 0:

            raise RuntimeError("No answerable queries " "were evaluated.")

        wins = sum(1 for item in comparisons if item.outcome == "WIN")

        ties = sum(1 for item in comparisons if item.outcome == "TIE")

        losses = sum(1 for item in comparisons if item.outcome == "LOSS")

        changed = sum(1 for item in comparisons if item.rewrite_changed)

        fallbacks = sum(1 for item in comparisons if item.rewrite_used_fallback)

        return QueryRewriteBenchmarkSummary(
            evaluated_queries=count,
            rewrites_changed=changed,
            rewrites_unchanged=(count - changed),
            rewrite_fallbacks=(fallbacks),
            wins=wins,
            ties=ties,
            losses=losses,
            win_rate=wins / count,
            loss_rate=losses / count,
            original_hit_at_3=(
                sum(item.original.hit_at_3 for item in comparisons) / count
            ),
            rewritten_hit_at_3=(
                sum(item.rewritten.hit_at_3 for item in comparisons) / count
            ),
            original_recall_at_3=(
                sum(item.original.recall_at_3 for item in comparisons) / count
            ),
            rewritten_recall_at_3=(
                sum(item.rewritten.recall_at_3 for item in comparisons) / count
            ),
            original_precision_at_3=(
                sum(item.original.precision_at_3 for item in comparisons) / count
            ),
            rewritten_precision_at_3=(
                sum(item.rewritten.precision_at_3 for item in comparisons) / count
            ),
            original_mrr=(
                sum(item.original.reciprocal_rank for item in comparisons) / count
            ),
            rewritten_mrr=(
                sum(item.rewritten.reciprocal_rank for item in comparisons) / count
            ),
            average_rewrite_latency_ms=(
                sum(item.rewrite_latency_ms for item in comparisons) / count
            ),
            average_original_retrieval_ms=(
                sum(item.original.retrieval_latency_ms for item in comparisons) / count
            ),
            average_rewritten_retrieval_ms=(
                sum(item.rewritten.retrieval_latency_ms for item in comparisons) / count
            ),
            average_rewritten_total_ms=(
                sum(item.rewritten_total_latency_ms for item in comparisons) / count
            ),
        )

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    @staticmethod
    def print_summary(
        report: QueryRewriteBenchmarkReport,
    ) -> None:

        summary = report.summary

        print()
        print()
        print("=" * 70)
        print("QUERY REWRITING BENCHMARK SUMMARY")
        print("=" * 70)

        print(f"Queries evaluated       : " f"{summary.evaluated_queries}")
        print(f"Rewrites changed        : " f"{summary.rewrites_changed}")
        print(f"Rewrites unchanged      : " f"{summary.rewrites_unchanged}")
        print(f"Rewrite fallbacks       : " f"{summary.rewrite_fallbacks}")
        print()
        print(f"Wins                    : " f"{summary.wins}")
        print(f"Ties                    : " f"{summary.ties}")
        print(f"Losses                  : " f"{summary.losses}")
        print(f"Win rate                : " f"{summary.win_rate:.3f}")
        print(f"Loss rate               : " f"{summary.loss_rate:.3f}")

        print()
        print("-" * 70)

        print(
            f"{'Metric':<28}" f"{'Original':>16}" f"{'Rewritten':>16}" f"{'Delta':>16}"
        )

        print("-" * 70)

        rows = [
            (
                "Hit@3",
                summary.original_hit_at_3,
                summary.rewritten_hit_at_3,
            ),
            (
                "Recall@3",
                summary.original_recall_at_3,
                summary.rewritten_recall_at_3,
            ),
            (
                "Precision@3",
                summary.original_precision_at_3,
                summary.rewritten_precision_at_3,
            ),
            (
                "MRR",
                summary.original_mrr,
                summary.rewritten_mrr,
            ),
        ]

        for (
            label,
            original,
            rewritten,
        ) in rows:

            print(
                f"{label:<28}"
                f"{original:>16.3f}"
                f"{rewritten:>16.3f}"
                f"{rewritten-original:>16.3f}"
            )

        print("-" * 70)

        print(
            f"Avg rewrite latency     : " f"{summary.average_rewrite_latency_ms:.2f} ms"
        )

        print(
            f"Avg original retrieval  : "
            f"{summary.average_original_retrieval_ms:.2f} ms"
        )

        print(
            f"Avg rewritten retrieval : "
            f"{summary.average_rewritten_retrieval_ms:.2f} ms"
        )

        print(
            f"Avg rewritten TOTAL     : " f"{summary.average_rewritten_total_ms:.2f} ms"
        )

        print("=" * 70)

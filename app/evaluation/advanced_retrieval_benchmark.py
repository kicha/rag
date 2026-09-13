from __future__ import annotations

from time import perf_counter
from typing import List, Literal

from pydantic import BaseModel

from app.evaluation.retrieval_benchmark import (
    GoldQuery,
)

from app.retrieval.hybrid_parent_child_retriever import (
    HybridParentChildRetriever,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

# ============================================================
# TYPES
# ============================================================

AdvancedStrategy = Literal[
    "hybrid_parent",
    "hybrid_crossencoder",
    "hybrid_crossencoder_mmr",
]


# ============================================================
# RESULT MODELS
# ============================================================


class RankedParent(BaseModel):

    rank: int

    parent_id: str

    document_id: str

    parent_index: int

    score: float | None = None


class AdvancedQueryMetrics(BaseModel):

    hit_at_3: float

    recall_at_3: float

    reciprocal_rank: float

    context_precision_at_3: float


class AdvancedQueryResult(BaseModel):

    query: str

    query_class: str

    relevant_docs: List[str]

    retrieved_parents: List[RankedParent]

    metrics: AdvancedQueryMetrics

    latency_ms: float


class AdvancedStrategySummary(BaseModel):

    strategy: AdvancedStrategy

    evaluated_queries: int

    hit_at_3: float

    recall_at_3: float

    mrr: float

    context_precision_at_3: float

    average_latency_ms: float


class AdvancedStrategyResult(BaseModel):

    strategy: AdvancedStrategy

    query_results: List[AdvancedQueryResult]

    summary: AdvancedStrategySummary


# ============================================================
# ADVANCED BENCHMARK EVALUATOR
# ============================================================


class AdvancedRetrievalBenchmarkEvaluator:

    def __init__(
        self,
        hybrid_parent_retriever: HybridParentChildRetriever,
        cross_encoder: CrossEncoderReranker,
        hybrid_rerank_mmr_retriever: HybridRerankMMRRetriever,
        hybrid_child_top_k: int = 30,
        cross_encoder_top_k: int = 10,
        final_top_k: int = 3,
    ) -> None:

        if hybrid_child_top_k <= 0:
            raise ValueError("hybrid_child_top_k must " "be greater than zero.")

        if cross_encoder_top_k <= 0:
            raise ValueError("cross_encoder_top_k must " "be greater than zero.")

        if final_top_k <= 0:
            raise ValueError("final_top_k must " "be greater than zero.")

        if final_top_k > cross_encoder_top_k:
            raise ValueError("final_top_k cannot exceed " "cross_encoder_top_k.")

        self.hybrid_parent_retriever = hybrid_parent_retriever

        self.cross_encoder = cross_encoder

        self.hybrid_rerank_mmr_retriever = hybrid_rerank_mmr_retriever

        self.hybrid_child_top_k = hybrid_child_top_k

        self.cross_encoder_top_k = cross_encoder_top_k

        self.final_top_k = final_top_k

    # ========================================================
    # METRICS
    # ========================================================

    @staticmethod
    def _hit_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        return 1.0 if set(retrieved_docs[:k]) & relevant_docs else 0.0

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

    @staticmethod
    def _reciprocal_rank(
        retrieved_docs: List[str],
        relevant_docs: set[str],
    ) -> float:

        for rank, document_id in enumerate(
            retrieved_docs,
            start=1,
        ):

            if document_id in relevant_docs:

                return 1.0 / rank

        return 0.0

    @staticmethod
    def _context_precision_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        if k <= 0:
            return 0.0

        retrieved_top_k = retrieved_docs[:k]

        if not retrieved_top_k:
            return 0.0

        relevant_count = sum(
            1 for document_id in retrieved_top_k if document_id in relevant_docs
        )

        return relevant_count / len(retrieved_top_k)

    # ========================================================
    # METRIC CALCULATION
    # ========================================================

    def _calculate_metrics(
        self,
        retrieved_docs: List[str],
        relevant_docs: List[str],
    ) -> AdvancedQueryMetrics:

        relevant_set = set(relevant_docs)

        return AdvancedQueryMetrics(
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
            reciprocal_rank=(
                self._reciprocal_rank(
                    retrieved_docs,
                    relevant_set,
                )
            ),
            context_precision_at_3=(
                self._context_precision_at_k(
                    retrieved_docs,
                    relevant_set,
                    3,
                )
            ),
        )

    # ========================================================
    # HYBRID PARENT
    # ========================================================

    def _run_hybrid_parent(
        self,
        query: str,
    ) -> List[RankedParent]:

        results = self.hybrid_parent_retriever.retrieve(
            query=query,
            child_top_k=(self.hybrid_child_top_k),
            parent_top_k=(self.final_top_k),
        )

        ranked: List[RankedParent] = []

        for rank, result in enumerate(
            results,
            start=1,
        ):

            parent = result.parent

            ranked.append(
                RankedParent(
                    rank=rank,
                    parent_id=str(parent.parent_id),
                    document_id=(parent.document_id),
                    parent_index=(parent.parent_index),
                    score=(result.best_score),
                )
            )

        return ranked

    # ========================================================
    # HYBRID + CROSSENCODER
    # ========================================================

    def _run_crossencoder(
        self,
        query: str,
    ) -> List[RankedParent]:

        candidates = self.hybrid_parent_retriever.retrieve(
            query=query,
            child_top_k=(self.hybrid_child_top_k),
            parent_top_k=None,
        )

        reranked = self.cross_encoder.rerank(
            query=query,
            candidates=candidates,
            top_k=(self.final_top_k),
        )

        ranked: List[RankedParent] = []

        for result in reranked.results:

            parent = result.result.parent

            ranked.append(
                RankedParent(
                    rank=(result.reranked_rank),
                    parent_id=str(parent.parent_id),
                    document_id=(parent.document_id),
                    parent_index=(parent.parent_index),
                    score=(result.reranker_score),
                )
            )

        return ranked

    # ========================================================
    # HYBRID + CROSSENCODER + MMR
    # ========================================================

    def _run_mmr(
        self,
        query: str,
    ) -> List[RankedParent]:

        results = self.hybrid_rerank_mmr_retriever.retrieve(
            query=query,
            child_top_k=(self.hybrid_child_top_k),
            cross_encoder_top_k=(self.cross_encoder_top_k),
            final_top_k=(self.final_top_k),
        )

        ranked: List[RankedParent] = []

        for result in results:

            parent = result.parent

            ranked.append(
                RankedParent(
                    rank=result.rank,
                    parent_id=str(parent.parent_id),
                    document_id=(parent.document_id),
                    parent_index=(parent.parent_index),
                    score=(result.mmr_score),
                )
            )

        return ranked

    # ========================================================
    # RUN STRATEGY
    # ========================================================

    def _retrieve(
        self,
        query: str,
        strategy: AdvancedStrategy,
    ) -> List[RankedParent]:

        if strategy == ("hybrid_parent"):

            return self._run_hybrid_parent(query)

        if strategy == ("hybrid_crossencoder"):

            return self._run_crossencoder(query)

        if strategy == ("hybrid_crossencoder_mmr"):

            return self._run_mmr(query)

        raise ValueError(f"Unknown strategy: " f"{strategy}")

    # ========================================================
    # ONE STRATEGY
    # ========================================================

    def evaluate_strategy(
        self,
        gold_queries: List[GoldQuery],
        strategy: AdvancedStrategy,
    ) -> AdvancedStrategyResult:

        print()
        print()
        print("=" * 100)
        print(f"ADVANCED STRATEGY: " f"{strategy.upper()}")
        print("=" * 100)

        query_results: List[AdvancedQueryResult] = []

        for index, gold in enumerate(
            gold_queries,
            start=1,
        ):

            if not gold.relevant_docs:

                print(f"\n[{index:02d}] " f"SKIP UNANSWERABLE: " f"{gold.query}")

                continue

            started = perf_counter()

            retrieved_parents = self._retrieve(
                query=gold.query,
                strategy=strategy,
            )

            latency_ms = (perf_counter() - started) * 1000.0

            retrieved_docs = [item.document_id for item in retrieved_parents]

            metrics = self._calculate_metrics(
                retrieved_docs=(retrieved_docs),
                relevant_docs=(gold.relevant_docs),
            )

            query_results.append(
                AdvancedQueryResult(
                    query=gold.query,
                    query_class=(gold.query_class),
                    relevant_docs=(gold.relevant_docs),
                    retrieved_parents=(retrieved_parents),
                    metrics=metrics,
                    latency_ms=latency_ms,
                )
            )

            print()
            print(f"[{index:02d}] " f"{gold.query}")

            print(f"Relevant : " f"{gold.relevant_docs}")

            print(f"Top 3    : " f"{retrieved_docs}")

            print(
                "Metrics  : "
                f"Hit@3="
                f"{metrics.hit_at_3:.0f}  "
                f"Recall@3="
                f"{metrics.recall_at_3:.3f}  "
                f"Precision@3="
                f"{metrics.context_precision_at_3:.3f}  "
                f"RR="
                f"{metrics.reciprocal_rank:.3f}"
            )

        summary = self._summarize(
            strategy=strategy,
            query_results=(query_results),
        )

        return AdvancedStrategyResult(
            strategy=strategy,
            query_results=(query_results),
            summary=summary,
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    @staticmethod
    def _summarize(
        strategy: AdvancedStrategy,
        query_results: List[AdvancedQueryResult],
    ) -> AdvancedStrategySummary:

        count = len(query_results)

        if count == 0:
            raise RuntimeError("No answerable queries.")

        return AdvancedStrategySummary(
            strategy=strategy,
            evaluated_queries=count,
            hit_at_3=sum(result.metrics.hit_at_3 for result in query_results) / count,
            recall_at_3=sum(result.metrics.recall_at_3 for result in query_results)
            / count,
            mrr=sum(result.metrics.reciprocal_rank for result in query_results) / count,
            context_precision_at_3=sum(
                result.metrics.context_precision_at_3 for result in query_results
            )
            / count,
            average_latency_ms=sum(result.latency_ms for result in query_results)
            / count,
        )

    # ========================================================
    # FULL BENCHMARK
    # ========================================================

    def evaluate(
        self,
        gold_queries: List[GoldQuery],
    ) -> List[AdvancedStrategyResult]:

        strategies: List[AdvancedStrategy] = [
            "hybrid_parent",
            "hybrid_crossencoder",
            "hybrid_crossencoder_mmr",
        ]

        return [
            self.evaluate_strategy(
                gold_queries=(gold_queries),
                strategy=strategy,
            )
            for strategy in strategies
        ]

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    @staticmethod
    def print_summary(
        results: List[AdvancedStrategyResult],
    ) -> None:

        print()
        print()
        print("=" * 120)
        print("ADVANCED RETRIEVAL " "BENCHMARK SUMMARY")
        print("=" * 120)

        print(
            f"{'Strategy':<32}"
            f"{'Hit@3':>10}"
            f"{'Recall@3':>12}"
            f"{'Precision@3':>15}"
            f"{'MRR':>10}"
            f"{'Avg ms':>12}"
        )

        print("-" * 120)

        for result in results:

            summary = result.summary

            print(
                f"{summary.strategy:<32}"
                f"{summary.hit_at_3:>10.3f}"
                f"{summary.recall_at_3:>12.3f}"
                f"{summary.context_precision_at_3:>15.3f}"
                f"{summary.mrr:>10.3f}"
                f"{summary.average_latency_ms:>12.2f}"
            )

        print("=" * 120)

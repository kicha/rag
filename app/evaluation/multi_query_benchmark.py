from __future__ import annotations

from time import perf_counter
from typing import List

from pydantic import BaseModel

from app.evaluation.retrieval_benchmark import (
    GoldQuery,
)

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)

from app.retrieval.hybrid_rerank_mmr_retriever import (
    HybridRerankMMRRetriever,
)

from app.retrieval.multi_query_hybrid_retriever import (
    MultiQueryHybridRetriever,
)

# ============================================================
# FINAL RETRIEVAL METRICS
# ============================================================


class FinalRetrievalMetrics(BaseModel):
    retrieved_documents: List[str]
    hit_at_3: float
    recall_at_3: float
    precision_at_3: float
    reciprocal_rank: float
    first_relevant_rank: int | None
    latency_ms: float


# ============================================================
# CANDIDATE DISCOVERY METRICS
# ============================================================


class CandidateMetrics(BaseModel):
    candidate_documents: List[str]
    candidate_parent_count: int
    candidate_document_count: int
    candidate_recall: float
    candidate_hit: float


# ============================================================
# PER QUERY
# ============================================================


class MultiQueryComparison(BaseModel):
    original_query: str
    query_class: str
    relevant_docs: List[str]
    generated_queries: List[str]
    generation_latency_ms: float
    generation_fallback: bool
    baseline_candidates: CandidateMetrics
    multi_query_candidates: CandidateMetrics
    baseline_final: FinalRetrievalMetrics
    multi_query_final: FinalRetrievalMetrics
    candidate_recall_delta: float
    final_recall_delta: float
    precision_delta: float
    reciprocal_rank_delta: float


# ============================================================
# SUMMARY
# ============================================================


class MultiQueryBenchmarkSummary(BaseModel):

    evaluated_queries: int

    baseline_candidate_recall: float
    multi_query_candidate_recall: float

    baseline_candidate_hit: float
    multi_query_candidate_hit: float

    baseline_hit_at_3: float
    multi_query_hit_at_3: float

    baseline_recall_at_3: float
    multi_query_recall_at_3: float

    baseline_precision_at_3: float
    multi_query_precision_at_3: float

    baseline_mrr: float
    multi_query_mrr: float

    avg_generation_latency_ms: float

    avg_baseline_latency_ms: float
    avg_multi_query_total_latency_ms: float


# ============================================================
# REPORT
# ============================================================


class MultiQueryBenchmarkReport(BaseModel):
    comparisons: List[MultiQueryComparison]
    summary: MultiQueryBenchmarkSummary


# ============================================================
# EVALUATOR
# ============================================================


class MultiQueryBenchmarkEvaluator:

    def __init__(
        self,
        hybrid_child_retriever: HybridChildRetriever,
        baseline_retriever: HybridRerankMMRRetriever,
        multi_query_retriever: MultiQueryHybridRetriever,
        baseline_child_top_k: int = 30,
        multi_child_top_k_per_query: int = 15,
        multi_fused_child_top_k: int = 30,
        cross_encoder_top_k: int = 10,
        final_top_k: int = 3,
    ) -> None:

        self.hybrid_child_retriever = hybrid_child_retriever
        self.baseline_retriever = baseline_retriever
        self.multi_query_retriever = multi_query_retriever
        self.baseline_child_top_k = baseline_child_top_k
        self.multi_child_top_k_per_query = multi_child_top_k_per_query
        self.multi_fused_child_top_k = multi_fused_child_top_k
        self.cross_encoder_top_k = cross_encoder_top_k
        self.final_top_k = final_top_k

    # ========================================================
    # UNIQUE ORDER-PRESERVING DOCUMENTS
    # ========================================================

    @staticmethod
    def _unique_documents(
        document_ids: List[str],
    ) -> List[str]:

        seen: set[str] = set()

        result: List[str] = []

        for document_id in document_ids:

            if not document_id:
                continue

            if document_id in seen:
                continue

            seen.add(document_id)

            result.append(document_id)

        return result

    # ========================================================
    # FIRST RELEVANT RANK
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

    # ========================================================
    # FINAL METRICS
    # ========================================================

    @classmethod
    def _final_metrics(
        cls,
        retrieved_docs: List[str],
        relevant_docs: List[str],
        latency_ms: float,
    ) -> FinalRetrievalMetrics:

        relevant_set = set(relevant_docs)

        first_rank = cls._first_relevant_rank(
            retrieved_docs,
            relevant_set,
        )

        top_3 = retrieved_docs[:3]

        found_unique = set(top_3) & relevant_set

        hit = 1.0 if found_unique else 0.0

        recall = len(found_unique) / len(relevant_set) if relevant_set else 0.0

        # -----------------------------------------------
        # Precision counts actual context slots.
        #
        # Two relevant ParentChunks from the same DOC
        # therefore count as two relevant slots.
        # -----------------------------------------------

        precision = (
            sum(1 for document_id in top_3 if document_id in relevant_set) / len(top_3)
            if top_3
            else 0.0
        )

        reciprocal_rank = 1.0 / first_rank if first_rank is not None else 0.0

        return FinalRetrievalMetrics(
            retrieved_documents=(retrieved_docs),
            hit_at_3=hit,
            recall_at_3=recall,
            precision_at_3=precision,
            reciprocal_rank=(reciprocal_rank),
            first_relevant_rank=(first_rank),
            latency_ms=(latency_ms),
        )

    # ========================================================
    # CANDIDATE METRICS
    # ========================================================

    @classmethod
    def _candidate_metrics(
        cls,
        document_ids: List[str],
        parent_count: int,
        relevant_docs: List[str],
    ) -> CandidateMetrics:

        unique_docs = cls._unique_documents(document_ids)

        relevant_set = set(relevant_docs)

        found = set(unique_docs) & relevant_set

        recall = len(found) / len(relevant_set) if relevant_set else 0.0

        hit = 1.0 if found else 0.0

        return CandidateMetrics(
            candidate_documents=(unique_docs),
            candidate_parent_count=(parent_count),
            candidate_document_count=(len(unique_docs)),
            candidate_recall=(recall),
            candidate_hit=(hit),
        )

    # ========================================================
    # BASELINE CANDIDATE DISCOVERY
    # ========================================================

    def _baseline_candidates(
        self,
        query: str,
        relevant_docs: List[str],
    ) -> CandidateMetrics:

        child_hits = self.hybrid_child_retriever.retrieve_hybrid(
            query=query,
            limit=(self.baseline_child_top_k),
        )

        # ----------------------------------------------------
        # Candidate parent count:
        # unique parent_id among retrieved children.
        # ----------------------------------------------------

        parent_ids: set[str] = set()

        document_ids: List[str] = []

        for hit in child_hits:
            payload = hit.payload or {}
            parent_id = payload.get("parent_id")
            document_id = payload.get("document_id")

            if parent_id:
                parent_ids.add(str(parent_id))

            if document_id:
                document_ids.append(str(document_id))

        return self._candidate_metrics(
            document_ids=(document_ids),
            parent_count=(len(parent_ids)),
            relevant_docs=(relevant_docs),
        )

    # ========================================================
    # BASELINE FINAL PIPELINE
    # ========================================================

    def _baseline_final(
        self,
        query: str,
        relevant_docs: List[str],
    ) -> FinalRetrievalMetrics:

        started = perf_counter()

        results = self.baseline_retriever.retrieve(
            query=query,
            child_top_k=(self.baseline_child_top_k),
            cross_encoder_top_k=(self.cross_encoder_top_k),
            final_top_k=(self.final_top_k),
        )

        latency_ms = (perf_counter() - started) * 1000.0

        retrieved_docs = [result.parent.document_id for result in results]

        return self._final_metrics(
            retrieved_docs=(retrieved_docs),
            relevant_docs=(relevant_docs),
            latency_ms=(latency_ms),
        )

    # ========================================================
    # ONE QUERY
    # ========================================================

    def evaluate_query(
        self,
        gold: GoldQuery,
    ) -> MultiQueryComparison:

        # ====================================================
        # 1. BASELINE CANDIDATE POOL
        #
        # Diagnostic run only.
        # NOT included in baseline latency.
        # ====================================================

        baseline_candidates = self._baseline_candidates(
            query=gold.query,
            relevant_docs=(gold.relevant_docs),
        )

        # ====================================================
        # 2. BASELINE COMPLETE PIPELINE
        # ====================================================

        baseline_final = self._baseline_final(
            query=gold.query,
            relevant_docs=(gold.relevant_docs),
        )

        # ====================================================
        # 3. MULTI-QUERY COMPLETE PIPELINE
        # ====================================================

        started = perf_counter()

        multi_result = self.multi_query_retriever.retrieve(
            query=gold.query,
            child_top_k_per_query=(self.multi_child_top_k_per_query),
            fused_child_top_k=(self.multi_fused_child_top_k),
            cross_encoder_top_k=(self.cross_encoder_top_k),
            final_top_k=(self.final_top_k),
        )

        multi_total_latency_ms = (perf_counter() - started) * 1000.0

        # ====================================================
        # 4. MULTI-QUERY CANDIDATE METRICS
        # ====================================================

        multi_candidates = self._candidate_metrics(
            document_ids=(multi_result.candidate_document_ids),
            parent_count=(multi_result.parent_candidates_before_rerank),
            relevant_docs=(gold.relevant_docs),
        )

        # ====================================================
        # 5. MULTI-QUERY FINAL METRICS
        # ====================================================

        multi_docs = [
            result.parent.document_id for result in multi_result.final_results
        ]

        multi_final = self._final_metrics(
            retrieved_docs=(multi_docs),
            relevant_docs=(gold.relevant_docs),
            latency_ms=(multi_total_latency_ms),
        )

        return MultiQueryComparison(
            original_query=(gold.query),
            query_class=(gold.query_class),
            relevant_docs=(gold.relevant_docs),
            generated_queries=(multi_result.generation.generated_queries),
            generation_latency_ms=(multi_result.generation.generation_latency_ms),
            generation_fallback=(multi_result.generation.used_fallback),
            baseline_candidates=(baseline_candidates),
            multi_query_candidates=(multi_candidates),
            baseline_final=(baseline_final),
            multi_query_final=(multi_final),
            candidate_recall_delta=(
                multi_candidates.candidate_recall - baseline_candidates.candidate_recall
            ),
            final_recall_delta=(multi_final.recall_at_3 - baseline_final.recall_at_3),
            precision_delta=(
                multi_final.precision_at_3 - baseline_final.precision_at_3
            ),
            reciprocal_rank_delta=(
                multi_final.reciprocal_rank - baseline_final.reciprocal_rank
            ),
        )

    # ========================================================
    # FULL BENCHMARK
    # ========================================================

    def evaluate(
        self,
        gold_queries: List[GoldQuery],
    ) -> MultiQueryBenchmarkReport:

        comparisons: List[MultiQueryComparison] = []

        for index, gold in enumerate(
            gold_queries,
            start=1,
        ):

            if not gold.relevant_docs:

                print()
                print(f"[{index:02d}] " f"SKIP UNANSWERABLE: " f"{gold.query}")

                continue

            comparison = self.evaluate_query(gold)

            comparisons.append(comparison)

            self._print_query(
                index=index,
                comparison=comparison,
            )

        summary = self._summarize(comparisons)

        return MultiQueryBenchmarkReport(
            comparisons=(comparisons),
            summary=summary,
        )

    # ========================================================
    # PRINT QUERY
    # ========================================================

    @staticmethod
    def _print_query(
        index: int,
        comparison: MultiQueryComparison,
    ) -> None:

        print()
        print("=" * 70)
        print(f"[{index:02d}] " f"{comparison.original_query}")
        print(f"Relevant docs      : " f"{comparison.relevant_docs}")
        print()
        print(
            "Baseline candidate : "
            f"{comparison.baseline_candidates.candidate_documents}"
        )
        print(
            "Multi candidate    : "
            f"{comparison.multi_query_candidates.candidate_documents}"
        )
        print(
            "Candidate recall   : "
            f"{comparison.baseline_candidates.candidate_recall:.3f}"
            " -> "
            f"{comparison.multi_query_candidates.candidate_recall:.3f}"
        )

        print()

        print(
            "Baseline final     : " f"{comparison.baseline_final.retrieved_documents}"
        )

        print(
            "Multi final        : "
            f"{comparison.multi_query_final.retrieved_documents}"
        )

        print(
            "Final Recall@3     : "
            f"{comparison.baseline_final.recall_at_3:.3f}"
            " -> "
            f"{comparison.multi_query_final.recall_at_3:.3f}"
        )

        print(
            "Final Precision@3  : "
            f"{comparison.baseline_final.precision_at_3:.3f}"
            " -> "
            f"{comparison.multi_query_final.precision_at_3:.3f}"
        )

        print(
            "MRR                : "
            f"{comparison.baseline_final.reciprocal_rank:.3f}"
            " -> "
            f"{comparison.multi_query_final.reciprocal_rank:.3f}"
        )

        print("Generation ms      : " f"{comparison.generation_latency_ms:.2f}")

    # ========================================================
    # SUMMARY
    # ========================================================

    @staticmethod
    def _summarize(
        comparisons: List[MultiQueryComparison],
    ) -> MultiQueryBenchmarkSummary:

        count = len(comparisons)

        if count == 0:

            raise RuntimeError("No answerable queries evaluated.")

        def average(
            values: List[float],
        ) -> float:

            return sum(values) / len(values)

        return MultiQueryBenchmarkSummary(
            evaluated_queries=count,
            baseline_candidate_recall=average(
                [item.baseline_candidates.candidate_recall for item in comparisons]
            ),
            multi_query_candidate_recall=average(
                [item.multi_query_candidates.candidate_recall for item in comparisons]
            ),
            baseline_candidate_hit=average(
                [item.baseline_candidates.candidate_hit for item in comparisons]
            ),
            multi_query_candidate_hit=average(
                [item.multi_query_candidates.candidate_hit for item in comparisons]
            ),
            baseline_hit_at_3=average(
                [item.baseline_final.hit_at_3 for item in comparisons]
            ),
            multi_query_hit_at_3=average(
                [item.multi_query_final.hit_at_3 for item in comparisons]
            ),
            baseline_recall_at_3=average(
                [item.baseline_final.recall_at_3 for item in comparisons]
            ),
            multi_query_recall_at_3=average(
                [item.multi_query_final.recall_at_3 for item in comparisons]
            ),
            baseline_precision_at_3=average(
                [item.baseline_final.precision_at_3 for item in comparisons]
            ),
            multi_query_precision_at_3=average(
                [item.multi_query_final.precision_at_3 for item in comparisons]
            ),
            baseline_mrr=average(
                [item.baseline_final.reciprocal_rank for item in comparisons]
            ),
            multi_query_mrr=average(
                [item.multi_query_final.reciprocal_rank for item in comparisons]
            ),
            avg_generation_latency_ms=average(
                [item.generation_latency_ms for item in comparisons]
            ),
            avg_baseline_latency_ms=average(
                [item.baseline_final.latency_ms for item in comparisons]
            ),
            avg_multi_query_total_latency_ms=average(
                [item.multi_query_final.latency_ms for item in comparisons]
            ),
        )

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    @staticmethod
    def print_summary(
        report: MultiQueryBenchmarkReport,
    ) -> None:

        s = report.summary

        print()
        print("=" * 70)
        print("MULTI-QUERY RETRIEVAL BENCHMARK SUMMARY")
        print("=" * 70)

        print(f"Queries evaluated: " f"{s.evaluated_queries}")

        print()
        print(
            f"{'Metric':<30}" f"{'Baseline':>15}" f"{'MultiQuery':>15}" f"{'Delta':>15}"
        )

        print("-" * 78)

        rows = [
            (
                "Candidate Recall",
                s.baseline_candidate_recall,
                s.multi_query_candidate_recall,
            ),
            (
                "Candidate Hit",
                s.baseline_candidate_hit,
                s.multi_query_candidate_hit,
            ),
            (
                "Hit@3",
                s.baseline_hit_at_3,
                s.multi_query_hit_at_3,
            ),
            (
                "Recall@3",
                s.baseline_recall_at_3,
                s.multi_query_recall_at_3,
            ),
            (
                "Precision@3",
                s.baseline_precision_at_3,
                s.multi_query_precision_at_3,
            ),
            (
                "MRR",
                s.baseline_mrr,
                s.multi_query_mrr,
            ),
        ]

        for (
            label,
            baseline,
            multi,
        ) in rows:

            print(
                f"{label:<30}"
                f"{baseline:>15.3f}"
                f"{multi:>15.3f}"
                f"{multi-baseline:>15.3f}"
            )

        print("-" * 78)

        print(
            f"Avg query-generation latency : " f"{s.avg_generation_latency_ms:.2f} ms"
        )

        print(f"Avg baseline retrieval       : " f"{s.avg_baseline_latency_ms:.2f} ms")

        print(
            f"Avg Multi-Query TOTAL        : "
            f"{s.avg_multi_query_total_latency_ms:.2f} ms"
        )

        print("=" * 70)

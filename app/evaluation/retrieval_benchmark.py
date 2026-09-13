from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Dict, List, Literal

from pydantic import BaseModel, Field
from qdrant_client.models import ScoredPoint

from app.retrieval.hybrid_child_retriever import (
    HybridChildRetriever,
)
from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

# ============================================================
# TYPES
# ============================================================

RetrievalStrategy = Literal[
    "dense",
    "sparse",
    "hybrid",
]


# ============================================================
# GOLD QUERY
# ============================================================


class GoldQuery(BaseModel):
    query: str

    relevant_docs: List[str] = Field(default_factory=list)

    query_class: str = ""


# ============================================================
# DOCUMENT SEARCH RESULT
# ============================================================


class RankedDocument(BaseModel):
    rank: int
    document_id: str
    best_score: float
    best_child_id: str | None = None
    best_child_index: int | None = None


# ============================================================
# PER-QUERY METRICS
# ============================================================


class QueryMetrics(BaseModel):
    hit_at_5: float
    hit_at_10: float

    recall_at_5: float
    recall_at_10: float

    reciprocal_rank: float


# ============================================================
# QUERY RESULT
# ============================================================


class QueryBenchmarkResult(BaseModel):
    query: str
    query_class: str
    relevant_docs: List[str]
    retrieved_documents: List[RankedDocument]
    metrics: QueryMetrics
    latency_ms: float


# ============================================================
# STRATEGY SUMMARY
# ============================================================


class StrategySummary(BaseModel):
    strategy: RetrievalStrategy

    evaluated_queries: int
    skipped_unanswerable_queries: int

    hit_at_5: float
    hit_at_10: float

    recall_at_5: float
    recall_at_10: float

    mrr: float

    average_latency_ms: float


# ============================================================
# STRATEGY RESULT
# ============================================================


class StrategyBenchmarkResult(BaseModel):
    strategy: RetrievalStrategy
    query_results: List[QueryBenchmarkResult]
    summary: StrategySummary


# ============================================================
# COMPLETE REPORT
# ============================================================


class RetrievalBenchmarkReport(BaseModel):
    collection_name: str
    qdrant_point_count: int
    total_gold_queries: int
    strategies: List[StrategyBenchmarkResult]


# ============================================================
# BENCHMARK EVALUATOR
# ============================================================


class RetrievalBenchmarkEvaluator:

    def __init__(
        self,
        retriever: HybridChildRetriever,
        vector_store: HybridQdrantStore,
        expected_point_count: int | None = None,
        child_candidate_limit: int = 50,
        document_limit: int = 10,
    ) -> None:

        if child_candidate_limit <= 0:
            raise ValueError("child_candidate_limit must " "be greater than zero.")

        if document_limit < 10:
            raise ValueError(
                "document_limit must be at least 10 "
                "because Recall@10 and Hit@10 "
                "are being evaluated."
            )

        self.retriever = retriever
        self.vector_store = vector_store
        self.expected_point_count = expected_point_count
        self.child_candidate_limit = child_candidate_limit
        self.document_limit = document_limit

    # ========================================================
    # COLLECTION VALIDATION
    # ========================================================

    def validate_collection(
        self,
    ) -> int:

        response = self.vector_store.client.count(
            collection_name=(self.vector_store.config.collection_name),
            exact=True,
        )

        point_count = int(response.count)

        print()
        print("=" * 80)
        print("QDRANT BENCHMARK VALIDATION")
        print("=" * 80)

        print(f"Collection : " f"{self.vector_store.config.collection_name}")

        print(f"Points     : " f"{point_count}")

        if (
            self.expected_point_count is not None
            and point_count != self.expected_point_count
        ):

            raise RuntimeError(
                "Unexpected Qdrant point count. "
                f"Expected "
                f"{self.expected_point_count}, "
                f"found {point_count}."
            )

        return point_count

    # ========================================================
    # PAYLOAD VALIDATION
    # ========================================================

    @staticmethod
    def _validate_hit_payload(
        hit: ScoredPoint,
    ) -> None:

        payload = hit.payload or {}

        document_id = payload.get("document_id")

        if not document_id:

            raise RuntimeError(
                "Retrieved Qdrant point does " "not contain document_id."
            )

        if not str(document_id).startswith("DOC-"):

            raise RuntimeError("Unexpected benchmark " f"document_id: {document_id}")

    # ========================================================
    # CHILD HITS -> UNIQUE DOCUMENTS
    # ========================================================

    def _collapse_to_documents(
        self,
        child_hits: List[ScoredPoint],
    ) -> List[RankedDocument]:

        documents: List[RankedDocument] = []

        seen_document_ids: set[str] = set()

        for hit in child_hits:

            self._validate_hit_payload(hit)

            payload = hit.payload or {}

            document_id = str(payload["document_id"])

            # ----------------------------------------------
            # Only the highest-ranked child for a document
            # determines that document's rank.
            # ----------------------------------------------

            if document_id in seen_document_ids:
                continue

            seen_document_ids.add(document_id)

            documents.append(
                RankedDocument(
                    rank=len(documents) + 1,
                    document_id=document_id,
                    best_score=float(hit.score),
                    best_child_id=(
                        str(payload.get("child_id"))
                        if payload.get("child_id") is not None
                        else None
                    ),
                    best_child_index=(payload.get("child_index")),
                )
            )

            if len(documents) >= self.document_limit:
                break

        return documents

    # ========================================================
    # RETRIEVE
    # ========================================================

    def _retrieve(
        self,
        query: str,
        strategy: RetrievalStrategy,
    ) -> List[RankedDocument]:

        if strategy == "dense":

            hits = self.retriever.retrieve_dense(
                query=query,
                limit=(self.child_candidate_limit),
            )

        elif strategy == "sparse":

            hits = self.retriever.retrieve_sparse(
                query=query,
                limit=(self.child_candidate_limit),
            )

        elif strategy == "hybrid":

            hits = self.retriever.retrieve_hybrid(
                query=query,
                limit=(self.child_candidate_limit),
            )

        else:

            raise ValueError(f"Unsupported strategy: " f"{strategy}")

        return self._collapse_to_documents(hits)

    # ========================================================
    # HIT
    # ========================================================

    @staticmethod
    def _hit_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        top_k = set(retrieved_docs[:k])

        return 1.0 if top_k & relevant_docs else 0.0

    # ========================================================
    # RECALL
    # ========================================================

    @staticmethod
    def _recall_at_k(
        retrieved_docs: List[str],
        relevant_docs: set[str],
        k: int,
    ) -> float:

        if not relevant_docs:
            return 0.0

        top_k = set(retrieved_docs[:k])

        relevant_retrieved = top_k & relevant_docs

        return len(relevant_retrieved) / len(relevant_docs)

    # ========================================================
    # RECIPROCAL RANK
    # ========================================================

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

    # ========================================================
    # QUERY METRICS
    # ========================================================

    def _calculate_metrics(
        self,
        retrieved_documents: List[RankedDocument],
        relevant_docs: List[str],
    ) -> QueryMetrics:

        retrieved_ids = [document.document_id for document in retrieved_documents]

        relevant_set = set(relevant_docs)

        return QueryMetrics(
            hit_at_5=self._hit_at_k(
                retrieved_docs=(retrieved_ids),
                relevant_docs=(relevant_set),
                k=5,
            ),
            hit_at_10=self._hit_at_k(
                retrieved_docs=(retrieved_ids),
                relevant_docs=(relevant_set),
                k=10,
            ),
            recall_at_5=(
                self._recall_at_k(
                    retrieved_docs=(retrieved_ids),
                    relevant_docs=(relevant_set),
                    k=5,
                )
            ),
            recall_at_10=(
                self._recall_at_k(
                    retrieved_docs=(retrieved_ids),
                    relevant_docs=(relevant_set),
                    k=10,
                )
            ),
            reciprocal_rank=(
                self._reciprocal_rank(
                    retrieved_docs=(retrieved_ids),
                    relevant_docs=(relevant_set),
                )
            ),
        )

    # ========================================================
    # ONE STRATEGY
    # ========================================================

    def evaluate_strategy(
        self,
        gold_queries: List[GoldQuery],
        strategy: RetrievalStrategy,
    ) -> StrategyBenchmarkResult:

        print()
        print()
        print("=" * 100)
        print(f"STRATEGY: " f"{strategy.upper()}")
        print("=" * 100)

        results: List[QueryBenchmarkResult] = []

        skipped_unanswerable = 0

        for index, gold in enumerate(
            gold_queries,
            start=1,
        ):

            # ----------------------------------------------
            # Queries with no relevant_docs represent
            # abstention/unanswerable tests.
            #
            # Hit/Recall/MRR are not defined meaningfully
            # for these, so skip them for these metrics.
            # ----------------------------------------------

            if not gold.relevant_docs:

                skipped_unanswerable += 1

                print(f"\n[{index:02d}] " f"SKIP UNANSWERABLE: " f"{gold.query}")

                continue

            started = perf_counter()

            retrieved_documents = self._retrieve(
                query=gold.query,
                strategy=strategy,
            )

            latency_ms = (perf_counter() - started) * 1000.0

            metrics = self._calculate_metrics(
                retrieved_documents=(retrieved_documents),
                relevant_docs=(gold.relevant_docs),
            )

            result = QueryBenchmarkResult(
                query=gold.query,
                query_class=(gold.query_class),
                relevant_docs=(gold.relevant_docs),
                retrieved_documents=(retrieved_documents),
                metrics=metrics,
                latency_ms=latency_ms,
            )

            results.append(result)

            top_ids = [item.document_id for item in retrieved_documents[:5]]

            print()
            print(f"[{index:02d}] " f"{gold.query}")
            print(f"Relevant : " f"{gold.relevant_docs}")
            print(f"Top 5    : " f"{top_ids}")
            print(
                "Metrics  : "
                f"Hit@5="
                f"{metrics.hit_at_5:.0f}  "
                f"Recall@5="
                f"{metrics.recall_at_5:.3f}  "
                f"RR="
                f"{metrics.reciprocal_rank:.3f}"
            )

        summary = self._summarize_strategy(
            strategy=strategy,
            results=results,
            skipped_unanswerable=(skipped_unanswerable),
        )

        return StrategyBenchmarkResult(
            strategy=strategy,
            query_results=results,
            summary=summary,
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    @staticmethod
    def _summarize_strategy(
        strategy: RetrievalStrategy,
        results: List[QueryBenchmarkResult],
        skipped_unanswerable: int,
    ) -> StrategySummary:

        count = len(results)

        if count == 0:

            raise RuntimeError("No answerable benchmark " "queries were evaluated.")

        return StrategySummary(
            strategy=strategy,
            evaluated_queries=count,
            skipped_unanswerable_queries=(skipped_unanswerable),
            hit_at_5=sum(item.metrics.hit_at_5 for item in results) / count,
            hit_at_10=sum(item.metrics.hit_at_10 for item in results) / count,
            recall_at_5=sum(item.metrics.recall_at_5 for item in results) / count,
            recall_at_10=sum(item.metrics.recall_at_10 for item in results) / count,
            mrr=sum(item.metrics.reciprocal_rank for item in results) / count,
            average_latency_ms=sum(item.latency_ms for item in results) / count,
        )

    # ========================================================
    # COMPLETE BENCHMARK
    # ========================================================

    def evaluate(
        self,
        gold_queries: List[GoldQuery],
    ) -> RetrievalBenchmarkReport:

        point_count = self.validate_collection()

        strategies: List[RetrievalStrategy] = [
            "dense",
            "sparse",
            "hybrid",
        ]

        strategy_results = []

        for strategy in strategies:

            result = self.evaluate_strategy(
                gold_queries=(gold_queries),
                strategy=strategy,
            )

            strategy_results.append(result)

        return RetrievalBenchmarkReport(
            collection_name=(self.vector_store.config.collection_name),
            qdrant_point_count=(point_count),
            total_gold_queries=len(gold_queries),
            strategies=(strategy_results),
        )

    # ========================================================
    # PRINT SUMMARY TABLE
    # ========================================================

    @staticmethod
    def print_summary(
        report: RetrievalBenchmarkReport,
    ) -> None:

        print()
        print()
        print("=" * 110)
        print("RETRIEVAL BENCHMARK SUMMARY")
        print("=" * 110)

        print(
            f"{'Strategy':<12}"
            f"{'Hit@5':>10}"
            f"{'Hit@10':>10}"
            f"{'Recall@5':>12}"
            f"{'Recall@10':>12}"
            f"{'MRR':>10}"
            f"{'Avg ms':>12}"
        )

        print("-" * 110)

        for result in report.strategies:

            summary = result.summary

            print(
                f"{summary.strategy:<12}"
                f"{summary.hit_at_5:>10.3f}"
                f"{summary.hit_at_10:>10.3f}"
                f"{summary.recall_at_5:>12.3f}"
                f"{summary.recall_at_10:>12.3f}"
                f"{summary.mrr:>10.3f}"
                f"{summary.average_latency_ms:>12.2f}"
            )

        print("=" * 110)

    # ========================================================
    # SAVE REPORT
    # ========================================================

    @staticmethod
    def save_report(
        report: RetrievalBenchmarkReport,
        output_path: Path,
    ) -> None:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            report.model_dump_json(indent=2),
            encoding="utf-8",
        )

        print(f"\nBenchmark report saved to: " f"{output_path}")


# ============================================================
# GOLD QUERY LOADER
# ============================================================


class GoldQueryLoader:

    @staticmethod
    def load(
        path: Path,
    ) -> List[GoldQuery]:

        if not path.exists():

            raise FileNotFoundError(f"Gold query file not found: " f"{path}")

        raw = json.loads(path.read_text(encoding="utf-8"))

        queries: List[GoldQuery] = []

        for item in raw:

            # Our generated file currently uses
            # "class" rather than "query_class".
            queries.append(
                GoldQuery(
                    query=item["query"],
                    relevant_docs=(
                        item.get(
                            "relevant_docs",
                            [],
                        )
                    ),
                    query_class=(
                        item.get(
                            "class",
                            "",
                        )
                    ),
                )
            )

        return queries

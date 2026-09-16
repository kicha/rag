from __future__ import annotations

from time import perf_counter
from typing import List

from langchain_core.language_models.chat_models import (
    BaseChatModel,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from pydantic import BaseModel, Field

# ============================================================
# STRUCTURED LLM OUTPUT
# ============================================================


class MultiQueryPayload(BaseModel):

    queries: List[str] = Field(
        description=(
            "Alternative retrieval queries that express "
            "different useful perspectives of the original "
            "user question."
        )
    )


# ============================================================
# PUBLIC RESULT
# ============================================================


class MultiQueryGenerationResult(BaseModel):
    original_query: str
    generated_queries: List[str]
    all_queries: List[str]
    generation_latency_ms: float
    used_fallback: bool = False
    error: str | None = None


# ============================================================
# GENERATOR
# ============================================================


class MultiQueryGenerator:

    SYSTEM_PROMPT = """
You are a query expansion component for a production
Retrieval-Augmented Generation system.

Given ONE original user query, generate several alternative
search queries that may retrieve complementary relevant
evidence.

Rules:

1. Preserve the user's original intent.

2. Do NOT answer the question.

3. Generate genuinely different retrieval perspectives.
   Do not merely make grammatical rewrites.

4. Preserve important:
   - identifiers
   - parameter names
   - acronyms
   - error codes
   - class names
   - model names
   - API names
   - product names

5. Do not invent unsupported facts.

6. Each query must be understandable independently.

7. Prefer retrieval-oriented terminology.

8. Different queries may emphasize:
   - mechanism
   - cause
   - effect
   - terminology
   - implementation
   - trade-offs

   but only when these remain faithful to the user's intent.

9. Do not make every query longer than the original merely
   for the sake of expansion.

10. Return only the requested number of alternative queries.

Example:

Original:
"How does HNSW avoid comparing every vector?"

Good alternatives:
- "How does HNSW graph traversal reduce exhaustive vector comparisons?"
- "How do HNSW hierarchy and graph navigation make nearest-neighbor search efficient?"
- "Why does HNSW search only a subset of vectors instead of scanning the full index?"

These are different retrieval perspectives, not three cosmetic
rewrites of the same sentence.
""".strip()

    def __init__(
        self,
        llm: BaseChatModel,
        generated_query_count: int = 3,
        include_original: bool = True,
        fail_open: bool = True,
    ) -> None:

        if generated_query_count <= 0:
            raise ValueError("generated_query_count must be greater than zero.")

        self.llm = llm
        self.generated_query_count = generated_query_count
        self.include_original = include_original
        self.fail_open = fail_open
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.SYSTEM_PROMPT,
                ),
                (
                    "human",
                    (
                        "Original query:\n"
                        "{query}\n\n"
                        "Generate exactly "
                        "{query_count} alternative "
                        "retrieval queries."
                    ),
                ),
            ]
        )

        self.structured_llm = self.llm.with_structured_output(MultiQueryPayload)

        self.chain = self.prompt | self.structured_llm

    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize(query: str) -> str:

        return " ".join(query.strip().split())

    # ========================================================
    # DEDUPLICATION
    # ========================================================

    @classmethod
    def _deduplicate(
        cls,
        queries: List[str],
    ) -> List[str]:

        seen: set[str] = set()
        unique: List[str] = []
        for query in queries:
            normalized = cls._normalize(query)

            if not normalized:
                continue

            key = normalized.casefold()
            if key in seen:
                continue

            seen.add(key)
            unique.append(normalized)

        return unique

    # ========================================================
    # GENERATE
    # ========================================================

    def generate(self, query: str) -> MultiQueryGenerationResult:

        original_query = self._normalize(query)

        if not original_query:
            raise ValueError("Query cannot be empty.")

        started = perf_counter()

        try:

            payload = self.chain.invoke(
                {
                    "query": original_query,
                    "query_count": (self.generated_query_count),
                }
            )

            generated_queries = self._deduplicate(payload.queries)

            # ------------------------------------------------
            # Never allow the original query to appear again
            # as one of the generated alternatives.
            # ------------------------------------------------

            generated_queries = [
                generated
                for generated in generated_queries
                if (generated.casefold() != original_query.casefold())
            ]

            # ------------------------------------------------
            # Bound the number of generated queries even if
            # the LLM returned more than requested.
            # ------------------------------------------------

            generated_queries = generated_queries[: self.generated_query_count]

            if not generated_queries:

                raise RuntimeError(
                    "Multi-query generator returned " "no usable alternative queries."
                )

            all_queries: List[str] = []

            if self.include_original:

                all_queries.append(original_query)

            all_queries.extend(generated_queries)

            latency_ms = (perf_counter() - started) * 1000.0

            return MultiQueryGenerationResult(
                original_query=(original_query),
                generated_queries=(generated_queries),
                all_queries=(all_queries),
                generation_latency_ms=(latency_ms),
                used_fallback=False,
                error=None,
            )

        except Exception as exc:

            latency_ms = (perf_counter() - started) * 1000.0

            if not self.fail_open:
                raise

            # ------------------------------------------------
            # Multi-query is an enhancement.
            #
            # On generation failure, preserve availability by
            # retrieving with the original query only.
            # ------------------------------------------------

            return MultiQueryGenerationResult(
                original_query=(original_query),
                generated_queries=[],
                all_queries=[original_query],
                generation_latency_ms=(latency_ms),
                used_fallback=True,
                error=str(exc),
            )

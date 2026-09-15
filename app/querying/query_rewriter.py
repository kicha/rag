from __future__ import annotations

from time import perf_counter

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# ============================================================
# STRUCTURED LLM OUTPUT
# ============================================================


class QueryRewritePayload(BaseModel):
    rewritten_query: str = Field(
        description=(
            "A retrieval-optimized version of the user's query. "
            "It must remain a question or search request and must "
            "not contain the answer."
        )
    )

    reason: str = Field(
        description=("A short explanation of what was clarified or preserved.")
    )


# ============================================================
# PUBLIC RESULT
# ============================================================


class QueryRewriteResult(BaseModel):
    original_query: str
    rewritten_query: str
    changed: bool
    reason: str
    latency_ms: float
    used_fallback: bool = False
    error: str | None = None


# ============================================================
# QUERY REWRITER
# ============================================================

# Include the below in the system prompt for the LLM:
# """Only rewrite when the original query is ambiguous,
# underspecified, context-dependent, or poorly formed.

# If the query is already specific and retrieval-ready,
# return it unchanged."""


class QueryRewriter:

    SYSTEM_PROMPT = """
You are a retrieval-query rewriting component in a production
Retrieval-Augmented Generation system.

Your task is to rewrite a user's query so that a search system
can retrieve relevant evidence more reliably.

Rules:

1. Do NOT answer the query.

2. Preserve the user's original intent.

3. Preserve important exact identifiers, acronyms, parameter
   names, product names, error codes, API names, class names,
   model names, and technical terms.

4. Expand vague wording only when the intended meaning can be
   reasonably inferred from the supplied query or context.

5. Do not invent facts that are not present in the query or
   supplied context.

6. Remove conversational filler that does not help retrieval.

7. Make implicit technical relationships explicit when doing
   so does not change the meaning.

8. Prefer one concise standalone retrieval query.

9. Do not produce multiple alternative queries. That belongs
   to the later Multi-Query Retrieval stage.

10. If the original query is already retrieval-ready, preserve
    it with little or no modification.

Examples:

Original:
"What about M?"

Context:
"We are discussing HNSW parameters."

Rewritten:
"How does the M parameter affect HNSW graph connectivity?"

Original:
"How does ef_construct affect HNSW graph quality?"

Rewritten:
"How does ef_construct affect HNSW graph quality?"

Original:
"What makes graph construction better?"

Context:
"We are discussing HNSW index construction and ef_construct."

Rewritten:
"How does ef_construct affect HNSW graph quality during index construction?"

Remember:
Rewrite for retrieval. Do not answer.
""".strip()

    def __init__(
        self,
        llm: BaseChatModel,
        fail_open: bool = True,
    ) -> None:

        self.llm = llm
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
                        "Optional conversation context:\n"
                        "{context}"
                    ),
                ),
            ]
        )

        # ----------------------------------------------------
        # Ask the model to return a validated Pydantic object.
        # ----------------------------------------------------

        self.structured_llm = self.llm.with_structured_output(QueryRewritePayload)

        self.chain = self.prompt | self.structured_llm

    # ========================================================
    # REWRITE
    # ========================================================

    def rewrite(
        self,
        query: str,
        context: str | None = None,
    ) -> QueryRewriteResult:

        original_query = query.strip()

        if not original_query:
            raise ValueError("Query cannot be empty.")

        context_text = context.strip() if context else "No additional context supplied."

        started = perf_counter()

        try:

            payload = self.chain.invoke(
                {
                    "query": original_query,
                    "context": context_text,
                }
            )

            rewritten_query = payload.rewritten_query.strip()

            if not rewritten_query:

                raise RuntimeError(
                    "Query rewriter returned " "an empty rewritten query."
                )

            latency_ms = (perf_counter() - started) * 1000.0

            changed = rewritten_query.casefold() != original_query.casefold()

            return QueryRewriteResult(
                original_query=original_query,
                rewritten_query=rewritten_query,
                changed=changed,
                reason=payload.reason.strip(),
                latency_ms=latency_ms,
                used_fallback=False,
                error=None,
            )

        except Exception as exc:

            latency_ms = (perf_counter() - started) * 1000.0

            if not self.fail_open:
                raise

            # ------------------------------------------------
            # Production principle:
            #
            # Query rewriting is an enhancement.
            # An unavailable LLM should not necessarily make
            # the entire retrieval system unavailable.
            #
            # Fall back to the original query while exposing
            # the failure in observability metadata.
            # ------------------------------------------------

            return QueryRewriteResult(
                original_query=original_query,
                rewritten_query=original_query,
                changed=False,
                reason=("Query rewriting failed; " "original query used."),
                latency_ms=latency_ms,
                used_fallback=True,
                error=str(exc),
            )

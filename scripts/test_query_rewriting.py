import os

from langchain_groq import ChatGroq

from app.querying.query_rewriter import (
    QueryRewriter,
)
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# TEST CASES
# ============================================================


TEST_CASES = [
    {
        "query": ("What makes graph construction better?"),
        "context": (
            "The discussion is about HNSW " "index construction and ef_construct."
        ),
    },
    {
        "query": ("What about M?"),
        "context": ("The discussion is about HNSW " "index parameters."),
    },
    {
        "query": ("How does ef_construct affect " "HNSW graph quality?"),
        "context": None,
    },
    {
        "query": ("Why don't we compare every vector?"),
        "context": ("The discussion is about HNSW " "nearest-neighbor search."),
    },
    {
        "query": ("metadata?"),
        "context": (
            "The discussion is about storing " "metadata alongside vectors in Qdrant."
        ),
    },
]


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY environment " "variable is not set.")

    # ========================================================
    # LLM
    # ========================================================

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_retries=2,
    )

    # ========================================================
    # QUERY REWRITER
    # ========================================================

    rewriter = QueryRewriter(
        llm=llm,
        fail_open=True,
    )

    # ========================================================
    # TEST
    # ========================================================

    print()
    print("=" * 100)
    print("QUERY REWRITING TEST")
    print("=" * 100)

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        result = rewriter.rewrite(
            query=test_case["query"],
            context=test_case["context"],
        )

        print()
        print("-" * 100)
        print(f"TEST {index}")
        print(f"Original  : " f"{result.original_query}")
        print(f"Rewritten : " f"{result.rewritten_query}")
        print(f"Changed   : " f"{result.changed}")
        print(f"Reason    : " f"{result.reason}")
        print(f"Latency   : " f"{result.latency_ms:.2f} ms")
        print(f"Fallback  : " f"{result.used_fallback}")

        if result.error:
            print(f"Error     : " f"{result.error}")

    print()
    print("=" * 100)


if __name__ == "__main__":
    main()

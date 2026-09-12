from types import SimpleNamespace

from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import EmbeddingService
from app.repositories.parent_repository import ParentRepository
from app.retrieval.parent_child_retriever import ParentChildRetriever
from app.vectorstore.qdrant_store import QdrantVectorStore

# ============================================================
# TEST HELPERS
# ============================================================


def print_test(
    name: str,
    passed: bool,
    details: str = "",
) -> None:

    status = "PASS" if passed else "FAIL"

    print(f"[{status}] {name}")

    if details:
        print(f"       {details}")


# ============================================================
# TEST 1
# NORMAL RETRIEVAL
# ============================================================


def test_normal_retrieval(
    retriever: ParentChildRetriever,
) -> None:

    query = "What does ef_construct control?"

    results = retriever.retrieve(query=query)

    passed = len(results) >= 1 and results[0].parent.parent_index == 5

    print_test(
        "Correct parent ranked first",
        passed,
        (
            f"parents={len(results)}, "
            f"top_parent_index="
            f"{results[0].parent.parent_index}"
            if results
            else "no results"
        ),
    )


# ============================================================
# TEST 2
# EMPTY QUERY
# ============================================================


def test_empty_query(
    retriever: ParentChildRetriever,
) -> None:

    try:

        retriever.retrieve(query="   ")

        print_test(
            "Empty query rejected",
            False,
            "Expected ValueError.",
        )

    except ValueError:

        print_test(
            "Empty query rejected",
            True,
        )


# ============================================================
# TEST 3
# SCORE THRESHOLD
# ============================================================


def test_score_threshold(
    retriever: ParentChildRetriever,
) -> None:

    query = "What does ef_construct control?"

    low_threshold_results = retriever.retrieve(
        query=query,
        child_top_k=5,
        child_score_threshold=0.0,
        parent_top_k=10,
    )

    high_threshold_results = retriever.retrieve(
        query=query,
        child_top_k=5,
        child_score_threshold=0.40,
        parent_top_k=10,
    )

    passed = len(high_threshold_results) < len(low_threshold_results)

    print_test(
        "Score threshold removes weak parents",
        passed,
        (
            f"threshold=0.0 -> "
            f"{len(low_threshold_results)} parents, "
            f"threshold=0.40 -> "
            f"{len(high_threshold_results)} parents"
        ),
    )


# ============================================================
# TEST 4
# PARENT DEDUPLICATION
# ============================================================


def test_parent_deduplication(
    retriever: ParentChildRetriever,
) -> None:

    query = "What metadata can be stored " "with vectors?"

    results = retriever.retrieve(
        query=query,
        child_top_k=5,
        child_score_threshold=0.40,
        parent_top_k=10,
    )

    parent_ids = [result.parent.parent_id for result in results]

    passed = len(parent_ids) == len(set(parent_ids))

    total_matched_children = sum(len(result.matched_children) for result in results)

    print_test(
        "Duplicate child hits collapse " "to unique parents",
        passed,
        (
            f"unique_parents="
            f"{len(parent_ids)}, "
            f"matched_children="
            f"{total_matched_children}"
        ),
    )


# ============================================================
# TEST 5
# PARENT TOP-K
# ============================================================


def test_parent_top_k(
    retriever: ParentChildRetriever,
) -> None:

    query = "How does HNSW search efficiently?"

    results = retriever.retrieve(
        query=query,
        child_top_k=10,
        child_score_threshold=0.0,
        parent_top_k=1,
    )

    passed = len(results) <= 1

    print_test(
        "parent_top_k limits final context",
        passed,
        (f"returned=" f"{len(results)}"),
    )


# ============================================================
# TEST 6
# VERY HIGH THRESHOLD
# ============================================================


def test_no_relevant_results(
    retriever: ParentChildRetriever,
) -> None:

    query = "What does ef_construct control?"

    results = retriever.retrieve(
        query=query,
        child_top_k=5,
        child_score_threshold=0.99,
        parent_top_k=5,
    )

    passed = len(results) == 0

    print_test(
        "Retriever can return zero results",
        passed,
        (f"returned=" f"{len(results)}"),
    )


# ============================================================
# FAKE COMPONENTS FOR FAILURE TEST
# ============================================================


class FakeEmbeddingService:

    def embed_query(
        self,
        query: str,
    ):

        # The vector is irrelevant for this test.
        return [
            0.0,
            0.0,
            0.0,
        ]


class FakeVectorStore:

    def search(
        self,
        query_vector,
        top_k: int,
    ):

        return [
            SimpleNamespace(
                id="fake-child-001",
                score=0.90,
                payload={
                    "child_id": "fake-child-001",
                    "parent_id": "parent-that-does-not-exist",
                    "document_id": "fake-document",
                    "child_index": 0,
                    "content": "Fake child content.",
                },
            )
        ]


class FakeParentRepository:

    def get_by_id(
        self,
        parent_id: str,
    ):

        return None


# ============================================================
# TEST 7
# DANGLING PARENT REFERENCE
# ============================================================


def test_dangling_parent_reference(
    config: ChunkingConfig,
) -> None:

    retriever = ParentChildRetriever(
        config=config,
        embedder=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
        parent_repository=FakeParentRepository(),
    )

    try:

        retriever.retrieve(
            query="test query",
            child_top_k=1,
            child_score_threshold=0.0,
            parent_top_k=1,
        )

        print_test(
            "Dangling parent reference detected",
            False,
            "Expected RuntimeError.",
        )

    except RuntimeError as error:

        passed = "Dangling ChildChunk reference" in str(error)

        print_test(
            "Dangling parent reference detected",
            passed,
            str(error),
        )


# ============================================================
# APPLICATION
# ============================================================


def main() -> None:

    print()
    print("=" * 72)
    print("PARENT / CHILD RETRIEVER " "BEHAVIOR TESTS")
    print("=" * 72)

    config = ChunkingConfig()

    embedder = EmbeddingService(config.embedding_model_name)

    vector_size = embedder.model.get_embedding_dimension()

    vector_store = QdrantVectorStore(
        config=config,
        vector_size=vector_size,
    )

    repository = ParentRepository(config=config)

    retriever = ParentChildRetriever(
        config=config,
        embedder=embedder,
        vector_store=vector_store,
        parent_repository=repository,
    )

    try:

        print()
        print("INTEGRATION TESTS")
        print("-" * 72)

        test_normal_retrieval(retriever)

        test_empty_query(retriever)

        test_score_threshold(retriever)

        test_parent_deduplication(retriever)

        test_parent_top_k(retriever)

        test_no_relevant_results(retriever)

        print()
        print("FAILURE TESTS")
        print("-" * 72)

        test_dangling_parent_reference(config)

    finally:

        repository.close()

    print()
    print("=" * 72)
    print("TEST RUN COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()

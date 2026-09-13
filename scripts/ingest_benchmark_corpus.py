from pathlib import Path
from time import perf_counter

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)

from app.ingestion.markdown_corpus_loader import (
    MarkdownCorpusLoader,
)

from app.ingestion.pipeline import (
    StructureAwareRAGDemo,
)

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    print()
    print("=" * 100)
    print("AGENTIC RAG — MODERATE CORPUS INGESTION")
    print("=" * 100)

    print(f"\nDocuments directory: " f"{DOCUMENTS_DIR}")

    # ========================================================
    # 1. CONFIG
    # ========================================================

    config = ChunkingConfig()
    hybrid_config = HybridSearchConfig()

    # ========================================================
    # 2. LOAD MARKDOWN DOCUMENTS
    # ========================================================

    loader = MarkdownCorpusLoader(documents_directory=DOCUMENTS_DIR)
    documents = loader.load()
    print(f"\nDocuments discovered: " f"{len(documents)}")

    for document in documents:
        print(f"  {document.document_id}" f" -> {document.source}")

    # ========================================================
    # 3. APPLICATION
    # ========================================================

    app = StructureAwareRAGDemo(
        config=config,
        hybrid_config=hybrid_config,
    )

    total_parents = 0
    total_children = 0

    succeeded = 0
    failed = 0

    started = perf_counter()

    try:

        # ====================================================
        # 4. INGEST ALL DOCUMENTS
        # ====================================================

        for index, document in enumerate(
            documents,
            start=1,
        ):

            print()
            print()
            print("#" * 100)
            print(f"DOCUMENT " f"{index}/{len(documents)}")
            print(f"ID     : " f"{document.document_id}")
            print(f"SOURCE : " f"{document.source}")
            print("#" * 100)
            document_started = perf_counter()

            try:

                result = app.ingest(
                    document=document,
                    # --------------------------------------
                    # IMPORTANT
                    #
                    # Recreate Qdrant only for the FIRST
                    # document.
                    #
                    # Every later document is appended to
                    # the same hybrid collection.
                    # --------------------------------------
                    recreate_hybrid_collection=(index == 1),
                )

                elapsed = perf_counter() - document_started
                parent_count = len(result.parents)
                child_count = len(result.children)
                total_parents += parent_count
                total_children += child_count
                succeeded += 1

                print()
                print("DOCUMENT COMPLETE")
                print(f"Parents  : " f"{parent_count}")
                print(f"Children : " f"{child_count}")
                print(f"Time     : " f"{elapsed:.2f}s")

            except Exception as exc:

                failed += 1
                print()
                print("DOCUMENT FAILED")
                print(f"Document ID : " f"{document.document_id}")
                print(f"Error       : " f"{exc}")

                # For benchmark creation I prefer
                # FAIL FAST.
                #
                # We do not want a silently incomplete
                # benchmark corpus.
                raise

    finally:

        app.close()

    # ========================================================
    # 5. FINAL SUMMARY
    # ========================================================

    total_elapsed = perf_counter() - started

    print()
    print()
    print("=" * 100)
    print("CORPUS INGESTION SUMMARY")
    print("=" * 100)
    print(f"\nDocuments discovered : " f"{len(documents)}")
    print(f"Documents succeeded  : " f"{succeeded}")
    print(f"Documents failed     : " f"{failed}")
    print(f"Total parents        : " f"{total_parents}")
    print(f"Total children       : " f"{total_children}")
    print(f"Total elapsed        : " f"{total_elapsed:.2f}s")
    print(f"\nHybrid collection    : " f"{hybrid_config.collection_name}")


if __name__ == "__main__":
    main()

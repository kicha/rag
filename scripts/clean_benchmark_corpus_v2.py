import logging
from pathlib import Path
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_DIRECTORY = PROJECT_ROOT / "data" / "documents"


BOILERPLATE_PARAGRAPH = (
    "Operationally, this topic should be validated with reproducible "
    "experiments rather than a single example. Record configuration, "
    "candidate counts, ranking order, identifiers, latency, and failure "
    "cases. Similar vocabulary can appear in neighboring retrieval topics, "
    "so evaluation should reward the most directly relevant document rather "
    "than any document that merely shares technical words."
)


def remove_boilerplate(
    text: str,
) -> tuple[str, int]:

    occurrence_count = text.count(BOILERPLATE_PARAGRAPH)

    cleaned_text = text.replace(
        f"{BOILERPLATE_PARAGRAPH}\n\n",
        "",
    )

    cleaned_text = cleaned_text.replace(
        f"{BOILERPLATE_PARAGRAPH}\n",
        "",
    )

    cleaned_text = cleaned_text.replace(
        BOILERPLATE_PARAGRAPH,
        "",
    )

    return (
        cleaned_text,
        occurrence_count,
    )


def main() -> None:

    configure_logging()
    markdown_files = sorted(DOCUMENTS_DIRECTORY.glob("DOC-*.md"))

    if not markdown_files:
        raise RuntimeError(
            f"No benchmark Markdown files found in " f"{DOCUMENTS_DIRECTORY}"
        )

    total_removed = 0
    changed_documents = 0

    for file_path in markdown_files:
        original_text = file_path.read_text(encoding="utf-8")
        cleaned_text, removed_count = remove_boilerplate(original_text)

        if removed_count == 0:
            logger.warning(f"document={file_path.name} " f"boilerplate_occurrences=0")

            continue

        file_path.write_text(
            cleaned_text,
            encoding="utf-8",
        )

        total_removed += removed_count
        changed_documents += 1

        logger.info(
            f"document={file_path.name} " f"removed_occurrences={removed_count}"
        )

    logger.info(
        f"documents_scanned={len(markdown_files)} "
        f"documents_changed={changed_documents} "
        f"total_removed_occurrences={total_removed}"
    )

    if total_removed != 96:
        raise RuntimeError(
            f"Expected to remove 96 boilerplate occurrences, "
            f"but removed {total_removed}."
        )

    if changed_documents != 24:
        raise RuntimeError(
            f"Expected to modify 24 documents, " f"but modified {changed_documents}."
        )

    logger.info("Benchmark corpus cleanup PASSED.")


if __name__ == "__main__":
    main()

import logging
import re
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


def normalize_text(
    text: str,
) -> str:

    return re.sub(
        r"\s+",
        " ",
        text.strip(),
    )


def remove_boilerplate(text: str) -> tuple[str, int]:

    paragraphs = re.split(
        r"\n\s*\n",
        text,
    )

    normalized_boilerplate = normalize_text(BOILERPLATE_PARAGRAPH)

    retained_paragraphs: list[str] = []
    removed_count = 0

    for paragraph in paragraphs:

        normalized_paragraph = normalize_text(paragraph)

        if normalized_paragraph == normalized_boilerplate:
            removed_count += 1
            continue

        retained_paragraphs.append(paragraph.strip())

    cleaned_text = (
        "\n\n".join(paragraph for paragraph in retained_paragraphs if paragraph).strip()
        + "\n"
    )

    return (
        cleaned_text,
        removed_count,
    )


def main() -> None:

    configure_logging()
    markdown_files = sorted(DOCUMENTS_DIRECTORY.glob("DOC-*.md"))

    if not markdown_files:
        raise RuntimeError(
            f"No benchmark Markdown files found in " f"{DOCUMENTS_DIRECTORY}"
        )

    cleaned_documents: dict[Path, str] = {}

    total_removed = 0
    changed_documents = 0

    # --------------------------------------------------------
    # PASS 1
    # Validate the entire migration before modifying files.
    # --------------------------------------------------------

    for file_path in markdown_files:
        original_text = file_path.read_text(encoding="utf-8")
        cleaned_text, removed_count = remove_boilerplate(original_text)

        logger.info(
            f"document={file_path.name} " f"boilerplate_occurrences={removed_count}"
        )

        if removed_count > 0:
            cleaned_documents[file_path] = cleaned_text
            changed_documents += 1
            total_removed += removed_count

    logger.info(
        f"documents_scanned={len(markdown_files)} "
        f"documents_to_change={changed_documents} "
        f"total_occurrences_to_remove={total_removed}"
    )

    # --------------------------------------------------------
    # Safety checks.
    #
    # No files have been modified yet.
    # --------------------------------------------------------

    if len(markdown_files) != 24:
        raise RuntimeError(
            f"Expected 24 benchmark documents, " f"but found {len(markdown_files)}."
        )

    if total_removed == 0:
        logger.info(
            "No boilerplate occurrences found. " "Benchmark corpus is already clean."
        )

    elif total_removed == 96:
        logger.info("Removed all 96 expected boilerplate occurrences.")

    else:
        raise RuntimeError(
            f"Unexpected partial corpus state. "
            f"Expected either 0 or 96 boilerplate occurrences, "
            f"but found {total_removed}."
        )

    # if changed_documents != 24:
    #     raise RuntimeError(
    #         f"Expected boilerplate in 24 documents, "
    #         f"but found it in {changed_documents}. "
    #         f"No files were modified."
    #     )

    # --------------------------------------------------------
    # PASS 2
    # Only modify files after the complete corpus validates.
    # --------------------------------------------------------

    for file_path, cleaned_text in cleaned_documents.items():

        file_path.write_text(
            cleaned_text,
            encoding="utf-8",
        )

        logger.info(f"cleaned_document={file_path.name}")

    logger.info(
        f"documents_scanned={len(markdown_files)} "
        f"documents_changed={changed_documents} "
        f"total_removed_occurrences={total_removed}"
    )

    logger.info("Benchmark corpus cleanup PASSED.")


if __name__ == "__main__":

    main()

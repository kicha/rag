import hashlib
import logging
import re
from collections import defaultdict
from pathlib import Path
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIRECTORY = PROJECT_ROOT / "data" / "documents"
MIN_PARAGRAPH_LENGTH = 80


def normalize_paragraph(paragraph: str) -> str:

    return re.sub(
        r"\s+",
        " ",
        paragraph.strip(),
    )


def split_paragraphs(text: str) -> list[str]:

    raw_paragraphs = re.split(r"\n\s*\n", text)

    return [
        normalize_paragraph(paragraph)
        for paragraph in raw_paragraphs
        if paragraph.strip()
    ]


def calculate_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:

    configure_logging()
    markdown_files = sorted(DOCUMENTS_DIRECTORY.glob("DOC-*.md"))

    if len(markdown_files) != 24:
        raise RuntimeError(
            f"Expected 24 benchmark documents, " f"found {len(markdown_files)}."
        )

    paragraph_locations: dict[
        str,
        list[tuple[str, int]],
    ] = defaultdict(list)

    document_ids: set[str] = set()

    total_characters = 0
    total_words = 0

    for file_path in markdown_files:
        text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            raise RuntimeError(f"Empty benchmark document: " f"{file_path.name}")

        match = re.match(
            r"^(DOC-\d+)",
            file_path.name,
            re.IGNORECASE,
        )

        if match is None:
            raise RuntimeError(f"Invalid benchmark filename: " f"{file_path.name}")

        document_id = match.group(1).upper()

        if document_id in document_ids:
            raise RuntimeError(f"Duplicate document_id: " f"{document_id}")

        document_ids.add(document_id)
        total_characters += len(text)

        total_words += len(re.findall(r"\b\w+\b", text))
        paragraphs = split_paragraphs(text)

        for paragraph_index, paragraph in enumerate(paragraphs):

            if len(paragraph) < MIN_PARAGRAPH_LENGTH:
                continue

            paragraph_locations[paragraph].append(
                (
                    file_path.name,
                    paragraph_index,
                )
            )

        logger.debug(f"document={file_path.name} " f"sha256={calculate_sha256(text)}")

    duplicate_groups = {
        paragraph: locations
        for paragraph, locations in paragraph_locations.items()
        if len(locations) > 1
    }

    logger.info(f"documents={len(markdown_files)}")
    logger.info(f"total_characters={total_characters}")
    logger.info(f"approx_words={total_words}")
    logger.info(f"exact_duplicate_paragraph_groups=" f"{len(duplicate_groups)}")

    if duplicate_groups:

        for paragraph, locations in duplicate_groups.items():

            logger.error(
                f"duplicate_paragraph=" f"{paragraph[:160]!r} " f"locations={locations}"
            )

        raise RuntimeError("Benchmark corpus contains repeated " "paragraphs.")

    logger.info("Benchmark corpus validation PASSED.")


if __name__ == "__main__":
    configure_logging()
    main()

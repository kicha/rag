import re
from pathlib import Path

DOCUMENT_ID_PATTERN = re.compile(
    r"^(DOC-\d+)",
    re.IGNORECASE,
)


def extract_document_id(
    file_path: Path,
) -> str:
    """
    Extract the benchmark document_id from a document filename.

    Expected filename format:

        DOC-001_hnsw_architecture_and_search.md
        DOC-024_retriever_benchmark_design.md

    Returns:

        DOC-001
        DOC-024

    Raises:
        ValueError:
            If the filename does not begin with a valid
            DOC-<number> prefix.
    """

    match = DOCUMENT_ID_PATTERN.match(file_path.name)

    if match is None:
        raise ValueError(
            f"Filename does not start with a valid "
            f"DOC-<number> prefix: {file_path.name}"
        )

    return match.group(1).upper()

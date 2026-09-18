import hashlib
import json
import logging
import re
from pathlib import Path

from pydantic import BaseModel
from app.utils.logging_config import configure_logging
from app.utils.document_id import extract_document_id

logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIRECTORY = PROJECT_ROOT / "data" / "documents"
BENCHMARK_DIRECTORY = PROJECT_ROOT / "data" / "benchmark"
GOLD_QUERIES_PATH = BENCHMARK_DIRECTORY / "gold_queries.json"
MANIFEST_PATH = BENCHMARK_DIRECTORY / "manifest.json"
BENCHMARK_VERSION = "2.0"


class DocumentManifestEntry(BaseModel):

    document_id: str
    source: str
    characters: int
    words: int
    sha256: str


class BenchmarkManifest(BaseModel):
    benchmark_version: str
    document_count: int
    gold_query_count: int
    total_characters: int
    approx_words: int
    corpus_sha256: str
    documents: list[DocumentManifestEntry]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_gold_query_count() -> int:

    with GOLD_QUERIES_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if isinstance(data, list):
        return len(data)

    if isinstance(data, dict):

        if "queries" in data:
            return len(data["queries"])

    raise RuntimeError("Unsupported gold_queries.json structure.")


def main() -> None:
    configure_logging()
    markdown_files = sorted(DOCUMENTS_DIRECTORY.glob("DOC-*.md"))
    document_entries: list[DocumentManifestEntry] = []
    corpus_hasher = hashlib.sha256()

    total_characters = 0
    total_words = 0

    for file_path in markdown_files:

        text = file_path.read_text(encoding="utf-8")

        word_count = len(
            re.findall(
                r"\b\w+\b",
                text,
            )
        )

        text_hash = sha256_text(text)

        document_entry = DocumentManifestEntry(
            document_id=(extract_document_id(file_path)),
            source=file_path.name,
            characters=len(text),
            words=word_count,
            sha256=text_hash,
        )

        document_entries.append(document_entry)
        total_characters += len(text)
        total_words += word_count

        corpus_hasher.update(document_entry.document_id.encode("utf-8"))
        corpus_hasher.update(b"\0")
        corpus_hasher.update(text.encode("utf-8"))
        corpus_hasher.update(b"\0")

    manifest = BenchmarkManifest(
        benchmark_version=(BENCHMARK_VERSION),
        document_count=len(document_entries),
        gold_query_count=(load_gold_query_count()),
        total_characters=(total_characters),
        approx_words=(total_words),
        corpus_sha256=(corpus_hasher.hexdigest()),
        documents=(document_entries),
    )

    MANIFEST_PATH.write_text(
        manifest.model_dump_json(indent=2),
        encoding="utf-8",
    )

    logger.info(f"benchmark_version=" f"{manifest.benchmark_version}")
    logger.info(f"document_count=" f"{manifest.document_count}")
    logger.info(f"gold_query_count=" f"{manifest.gold_query_count}")
    logger.info(f"total_characters=" f"{manifest.total_characters}")
    logger.info(f"approx_words=" f"{manifest.approx_words}")
    logger.info(f"corpus_sha256=" f"{manifest.corpus_sha256}")
    logger.info(f"manifest_written=" f"{MANIFEST_PATH}")


if __name__ == "__main__":

    main()

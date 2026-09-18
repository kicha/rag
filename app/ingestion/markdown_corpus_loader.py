import logging
import re
from pathlib import Path

from app.models.document import Document
from app.utils.document_id import extract_document_id

logger = logging.getLogger(__name__)


class MarkdownCorpusLoader:
    """
    Loads Markdown benchmark documents into the internal
    Document model.

    Expected naming convention:

        DOC-001_hnsw_architecture_and_search.md
        DOC-002_hnsw_construction_and_ef_construct.md

    The DOC-xxx prefix becomes the stable document_id.
    """

    def __init__(self, documents_directory: str | Path) -> None:
        self.documents_directory = Path(documents_directory)

    def load(self) -> list[Document]:

        self._validate_documents_directory()
        markdown_files = sorted(self.documents_directory.glob("DOC-*.md"))
        if not markdown_files:
            raise RuntimeError(
                f"No DOC-*.md files found in " f"{self.documents_directory}"
            )

        documents: list[Document] = []
        seen_document_ids: set[str] = set()

        for file_path in markdown_files:
            document = self._load_file(file_path)
            if document.document_id in seen_document_ids:
                raise RuntimeError(
                    f"Duplicate document_id detected: " f"{document.document_id}"
                )

            seen_document_ids.add(document.document_id)

            documents.append(document)

        logger.info(
            f"Loaded {len(documents)} Markdown documents "
            f"from {self.documents_directory}"
        )

        return documents

    def _validate_documents_directory(self) -> None:
        if not self.documents_directory.exists():
            raise FileNotFoundError(
                f"Documents directory does not exist: " f"{self.documents_directory}"
            )

        if not self.documents_directory.is_dir():
            raise NotADirectoryError(
                f"Expected a directory: " f"{self.documents_directory}"
            )

    def _load_file(self, file_path: Path) -> Document:
        document_id = extract_document_id(file_path)
        text = file_path.read_text(encoding="utf-8")
        if not text.strip():
            raise RuntimeError(f"Markdown document is empty: " f"{file_path}")

        document = Document(
            document_id=document_id,
            source=file_path.name,
            text=text,
        )

        logger.debug(
            f"Loaded document_id={document.document_id} " f"source={document.source}"
        )

        return document

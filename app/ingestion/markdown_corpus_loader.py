from pathlib import Path
import re
from typing import List

from app.models.document import Document


class MarkdownCorpusLoader:
    """
    Loads a directory of Markdown files into our internal
    Document model.

    Expected file naming convention:

        DOC-001_hnsw_architecture_and_search.md
        DOC-002_hnsw_construction_and_ef_construct.md
        ...

    The DOC-xxx prefix becomes the stable document_id.
    """

    DOCUMENT_ID_PATTERN = re.compile(
        r"^(DOC-\d+)",
        re.IGNORECASE,
    )

    def __init__(
        self,
        documents_directory: str | Path,
    ) -> None:

        self.documents_directory = Path(documents_directory)

    # ========================================================
    # LOAD ALL
    # ========================================================

    def load(self) -> List[Document]:

        if not self.documents_directory.exists():

            raise FileNotFoundError(
                "Documents directory does not exist: " f"{self.documents_directory}"
            )

        if not self.documents_directory.is_dir():

            raise NotADirectoryError(
                "Expected a directory: " f"{self.documents_directory}"
            )

        markdown_files = sorted(self.documents_directory.glob("DOC-*.md"))

        if not markdown_files:

            raise RuntimeError(
                "No DOC-*.md files found in " f"{self.documents_directory}"
            )

        documents: List[Document] = []

        seen_document_ids: set[str] = set()

        for file_path in markdown_files:

            document = self._load_file(file_path)

            if document.document_id in seen_document_ids:

                raise RuntimeError(
                    "Duplicate document_id detected: " f"{document.document_id}"
                )

            seen_document_ids.add(document.document_id)

            documents.append(document)

        return documents

    # ========================================================
    # LOAD ONE FILE
    # ========================================================

    def _load_file(
        self,
        file_path: Path,
    ) -> Document:

        document_id = self._extract_document_id(file_path)

        text = file_path.read_text(encoding="utf-8")

        if not text.strip():

            raise RuntimeError("Markdown document is empty: " f"{file_path}")

        return Document(
            document_id=document_id,
            # Keep the actual filename as source.
            source=file_path.name,
            text=text,
        )

    # ========================================================
    # DOCUMENT ID
    # ========================================================

    def _extract_document_id(
        self,
        file_path: Path,
    ) -> str:

        match = self.DOCUMENT_ID_PATTERN.match(file_path.name)

        if match is None:

            raise ValueError(
                "Markdown filename does not start " "with DOC-xxx: " f"{file_path.name}"
            )

        return match.group(1).upper()

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)
from app.repositories.parent_repository import ParentRepository
from app.utils.logging_config import configure_logging
from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "benchmark" / "benchmark_v2_units.json"


class ChildExport(BaseModel):
    child_id: str
    child_key: str
    child_index: int
    parent_id: str
    parent_key: str
    document_id: str
    content: str


class ParentExport(BaseModel):
    parent_id: str
    parent_key: str
    parent_index: int
    document_id: str
    section_path: list[str]
    content: str
    children: list[ChildExport]


class BenchmarkUnitsExport(BaseModel):
    benchmark_version: str
    parent_count: int
    child_count: int
    parents: list[ParentExport]


class BenchmarkV2UnitExporter:
    """
    Export the frozen Benchmark V2 persistence universe.

    MongoDB is authoritative for ParentChunks.

    Qdrant is authoritative for ChildChunk retrieval payloads.

    The output is intended for:
        - gold judgment authoring
        - manual inspection
        - benchmark debugging
        - future reproducibility
    """

    def __init__(
        self,
        chunking_config: ChunkingConfig,
        hybrid_config: HybridSearchConfig,
    ) -> None:

        self.chunking_config = chunking_config
        self.hybrid_config = hybrid_config

        self.parent_repository = ParentRepository(chunking_config)

        qdrant_url = (
            f"http://{chunking_config.qdrant_host}:" f"{chunking_config.qdrant_port}"
        )

        self.qdrant_client = QdrantClient(url=qdrant_url)

    def export(self) -> BenchmarkUnitsExport:
        parents = self._load_parents()
        children = self._load_children()
        children_by_parent_key: dict[
            str,
            list[ChildExport],
        ] = {}

        for child in children:

            children_by_parent_key.setdefault(
                child.parent_key,
                [],
            ).append(child)

        exported_parents: list[ParentExport] = []

        for parent in parents:

            parent_children = children_by_parent_key.get(
                parent.parent_key,
                [],
            )

            parent_children = sorted(
                parent_children,
                key=lambda child: child.child_index,
            )

            exported_parents.append(
                ParentExport(
                    parent_id=parent.parent_id,
                    parent_key=parent.parent_key,
                    parent_index=parent.parent_index,
                    document_id=parent.document_id,
                    section_path=parent.section_path,
                    content=parent.content,
                    children=parent_children,
                )
            )

        result = BenchmarkUnitsExport(
            benchmark_version="2.0",
            parent_count=len(exported_parents),
            child_count=len(children),
            parents=exported_parents,
        )

        logger.info(f"parent_count={result.parent_count}")
        logger.info(f"child_count={result.child_count}")

        return result

    def _load_parents(
        self,
    ) -> list[Any]:

        documents = list(self.parent_repository.collection.find({}))

        parents = [
            self.parent_repository._from_document(document) for document in documents
        ]

        parents.sort(
            key=lambda parent: (
                parent.document_id,
                parent.parent_index,
            )
        )

        return parents

    def _load_children(
        self,
    ) -> list[ChildExport]:

        children: list[ChildExport] = []

        next_offset = None

        while True:

            points, next_offset = self.qdrant_client.scroll(
                collection_name=(self.hybrid_config.collection_name),
                limit=100,
                offset=next_offset,
                with_payload=True,
                with_vectors=False,
            )

            for point in points:

                payload = point.payload

                if payload is None:
                    raise RuntimeError(
                        f"Qdrant point has no payload: " f"point_id={point.id}"
                    )

                children.append(
                    ChildExport(
                        child_id=payload["child_id"],
                        child_key=payload["child_key"],
                        child_index=payload["child_index"],
                        parent_id=payload["parent_id"],
                        parent_key=payload["parent_key"],
                        document_id=payload["document_id"],
                        content=payload["content"],
                    )
                )

            if next_offset is None:
                break

        children.sort(
            key=lambda child: (
                child.document_id,
                child.parent_key,
                child.child_index,
            )
        )

        return children

    def close(
        self,
    ) -> None:

        self.parent_repository.close()


def main() -> None:

    chunking_config = ChunkingConfig()

    hybrid_config = HybridSearchConfig()

    exporter = BenchmarkV2UnitExporter(
        chunking_config=chunking_config,
        hybrid_config=hybrid_config,
    )

    try:

        result = exporter.export()

        OUTPUT_PATH.write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )

        logger.info(f"benchmark_units_written={OUTPUT_PATH}")

    finally:

        exporter.close()


if __name__ == "__main__":

    configure_logging()
    main()

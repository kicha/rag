import logging

from app.models.metadata import (
    ChunkMetadata,
    ContentType,
    HeadingContext,
)
from app.models.parent_chunk import ParentChunk
from app.models.child_chunk import ChildChunk

logger = logging.getLogger(__name__)


def main() -> None:

    heading_context = HeadingContext(
        h1="Vector Databases",
        h2="HNSW",
        h3="ef_construct",
    )

    parent_content = (
        "The ef_construct parameter controls how broadly "
        "the graph is explored during index construction."
    )

    parent_hash = ParentChunk.create_content_hash(parent_content)

    parent_key = ParentChunk.create_parent_key(
        document_id="DOC-002",
        parent_index=3,
        section_path=heading_context.get_section_path(),
        content_hash=parent_hash,
    )

    parent = ParentChunk(
        document_id="DOC-002",
        content=parent_content,
        content_type=ContentType.TEXT,
        source="DOC-002_hnsw.md",
        heading_context=heading_context,
        metadata=ChunkMetadata(
            source_type="markdown",
            ingestion_version="benchmark_v2",
            char_count=len(parent_content),
            chunking_strategy="structure_aware_parent",
            chunking_version="parent_v2",
            content_type=ContentType.TEXT,
        ),
        content_hash=parent_hash,
        parent_index=3,
        parent_key=parent_key,
    )

    child_content = (
        "The ef_construct parameter controls graph exploration "
        "during index construction."
    )

    child_hash = ChildChunk.create_content_hash(child_content)

    child_key = ChildChunk.create_child_key(
        parent_key=parent.parent_key,
        child_index=0,
        content_hash=child_hash,
    )

    child = ChildChunk(
        document_id=parent.document_id,
        content=child_content,
        content_type=parent.content_type,
        source=parent.source,
        heading_context=parent.heading_context.model_copy(deep=True),
        metadata=parent.metadata.model_copy(deep=True),
        content_hash=child_hash,
        parent_id=parent.parent_id,
        parent_key=parent.parent_key,
        child_index=0,
        child_key=child_key,
    )

    logger.info("Parent runtime ID : %s", parent.parent_id)
    logger.info("Parent stable key : %s", parent.parent_key)
    logger.info("Parent section    : %s", parent.section_path)

    logger.info("Child runtime ID  : %s", child.child_id)
    logger.info("Child stable key  : %s", child.child_key)
    logger.info("Child parent ID   : %s", child.parent_id)
    logger.info("Child parent key  : %s", child.parent_key)

    assert child.parent_id == parent.parent_id
    assert child.parent_key == parent.parent_key
    assert parent.parent_key in child.child_key

    # Heading hierarchy must live only in HeadingContext.
    metadata_dump = parent.metadata.model_dump()

    assert "h1" not in metadata_dump
    assert "h2" not in metadata_dump
    assert "h3" not in metadata_dump
    assert "section_path" not in metadata_dump

    logger.info("Phase I model validation PASSED.")


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | %(levelname)-8s | " "%(name)s | %(message)s"),
    )

    main()

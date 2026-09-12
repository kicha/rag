from app.config.settings import ChunkingConfig
from app.ingestion.pipeline import StructureAwareRAGDemo
from scripts.test_parent_chunking import DemoDocumentFactory
from app.chunking.structure_aware_parent import StructureAwareParentChunker

# ============================================================
# MAIN
# ============================================================


def main():

    config = ChunkingConfig(
        max_chunk_chars=300,
        min_chunk_chars=100,
        embedding_model_name=("all-MiniLM-L6-v2"),
        qdrant_host="localhost",
        qdrant_port=6333,
        collection_name=("structure_aware_v3"),
        top_k=5,
    )

    app = StructureAwareRAGDemo(config)

    document = DemoDocumentFactory.create()

    app.ingest(document)

    queries = [
        "What is semantic chunking?",
        "How does Qdrant store vectors?",
        "How does retrieval work in RAG?",
        "What are the advantages of structure-aware chunking?",
    ]

    for query in queries:

        app.search(query)

    chunker = StructureAwareParentChunker(config)

    parents = chunker.chunk(
        document=document,
        elements=app.detector.detect(document),
    )
    print("=" * 70)
    print("STRUCTURE-AWARE PARENT CHUNKS")
    print("=" * 70)

    for parent in parents:
        print()
        print("PARENT ID     :", parent.parent_id)
        print("PARENT INDEX  :", parent.parent_index)
        print("DOCUMENT ID   :", parent.document_id)
        print("CONTENT TYPE  :", parent.content_type)
        print("SOURCE        :", parent.source)
        print("SECTION PATH  :", parent.section_path)
        print("CHAR COUNT    :", parent.char_count)
        print("CONTENT HASH  :", parent.content_hash)
        print("-" * 70)
        print(parent.content)


if __name__ == "__main__":

    main()

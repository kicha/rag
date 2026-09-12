from app.config.settings import ChunkingConfig
from app.ingestion.pipeline import StructureAwareRAGDemo
from scripts.test_parent_chunking import DemoDocumentFactory
from app.chunking.structure_aware_parent import StructureAwareParentChunker
from app.repositories.parent_repository import ParentRepository
from app.chunking.child_chunker import ChildChunker
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantVectorStore

# ============================================================
# MAIN
# ============================================================


def main():

    config = ChunkingConfig(
        max_chunk_chars=300,
        min_chunk_chars=100,
        embedding_model_name=("sentence-transformers/all-MiniLM-L6-v2"),
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

    # for query in queries:
    #     app.search(query)

    chunker = StructureAwareParentChunker(config)

    parents = chunker.chunk(
        document=document,
        elements=app.detector.detect(document),
    )
    # print("=" * 70)
    # print("STRUCTURE-AWARE PARENT CHUNKS")
    # print("=" * 70)

    # for parent in parents:
    #     print()
    #     print("PARENT ID     :", parent.parent_id)
    #     print("PARENT INDEX  :", parent.parent_index)
    #     print("DOCUMENT ID   :", parent.document_id)
    #     print("CONTENT TYPE  :", parent.content_type)
    #     print("SOURCE        :", parent.source)
    #     print("SECTION PATH  :", parent.section_path)
    #     print("CHAR COUNT    :", parent.char_count)
    #     print("CONTENT HASH  :", parent.content_hash)
    #     print("-" * 70)
    #     print(parent.content)
    # print("\n" + "=" * 70)
    # print("PARENT IDENTITY CHECK")
    # print("=" * 70)

    # for parent in parents:
    #     print(
    #         f"index={parent.parent_index} | "
    #         f"parent_id={parent.parent_id} | "
    #         f"hash={parent.content_hash}"
    #     )

    # print(f"\nTotal parents: {len(parents)}")
    # print(f"Unique parent IDs: {len({p.parent_id for p in parents})}")
    # print(f"Unique content hashes: {len({p.content_hash for p in parents})}")

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

    # ============================================================
    # MONGODB PARENT PERSISTENCE
    # ============================================================
    """
    repository = ParentRepository(config)

    try:

        print()
        print("=" * 70)
        print("MONGODB")
        print("=" * 70)

        repository.ping()

        print("\nMongoDB connection successful.")

        # --------------------------------------------------------
        # CLEAN ONLY THIS DEMO DOCUMENT
        # --------------------------------------------------------

        # deleted = repository.delete_by_document_id(document.document_id)

        # print(f"Existing parents deleted: {deleted}")

        # --------------------------------------------------------
        # INSERT PARENTS
        # --------------------------------------------------------

        inserted = repository.upsert_parents(parents)

        print(f"Parents inserted: {inserted}")

        # --------------------------------------------------------
        # VERIFY COUNT
        # --------------------------------------------------------

        stored_count = repository.count_by_document_id(document.document_id)

        print(f"Parents in MongoDB: {stored_count}")

        # --------------------------------------------------------
        # READ THEM BACK
        # --------------------------------------------------------

        stored_parents = repository.get_by_document_id(document.document_id)

        print()
        print("=" * 70, "PARENTS READ BACK FROM MONGODB", "=" * 70)

        for parent in stored_parents:

            print()

            print(
                "PARENT INDEX :",
                parent.parent_index,
            )
            print(
                "PARENT ID    :",
                parent.parent_id,
            )
            print(
                "HASH         :",
                parent.content_hash,
            )
            print(
                "SECTION      :",
                parent.section_path,
            )

    finally:

        repository.close()
    """

    repository = ParentRepository(config)

    try:

        repository.ping()
        # inserted = repository.upsert_parents(parents)
        sync_result = repository.sync_parents(
            document_id=document.document_id,
            parents=parents,
        )

        print()
        print("=" * 70)
        print("PARENT SYNCHRONIZATION")
        print("=" * 70)

        print("Incoming parents       :", sync_result.incoming_count)
        print("Existing before sync   :", sync_result.existing_count_before)
        print("New parents inserted   :", sync_result.inserted_count)
        print("Unchanged parents      :", sync_result.unchanged_count)
        print("Stale parents deleted  :", sync_result.deleted_stale_count)
        print("Parents after sync     :", sync_result.final_count)

        # print(f"New parents inserted: {inserted}")
        stored_count = repository.count_by_document_id(document.document_id)
        print(f"Parents currently in MongoDB: {stored_count}")

        stored_parents = repository.get_by_document_id(document.document_id)
        # ============================================================
        # CHILD CHUNKING EXPERIMENT
        # ============================================================

        child_chunker = ChildChunker(config)

        children = child_chunker.chunk_parents(stored_parents)

        print()
        print("=" * 70)
        print("CHILD CHUNKING SUMMARY")
        print("=" * 70)

        print("Stored parents :", len(stored_parents))
        print("Children       :", len(children))
        print()
        print("=" * 70)
        print("PARENT → CHILD LINKAGE")
        print("=" * 70)

        for parent in stored_parents:

            parent_children = [
                child for child in children if child.parent_id == parent.parent_id
            ]

            print()
            print("-" * 70)

            print("PARENT INDEX :", parent.parent_index)
            print("PARENT ID    :", parent.parent_id)
            print("PARENT CHARS :", parent.char_count)
            print("CHILD COUNT  :", len(parent_children))

            print("SECTION      :", parent.section_path)

            for child in parent_children:
                print()
                print("    CHILD INDEX :", child.child_index)
                print("    CHILD ID    :", child.child_id)
                print("    PARENT ID   :", child.parent_id)
                print("    CHARS       :", child.char_count)
                print("    HASH        :", child.content_hash)
                print("    CONTENT     :", repr(child.content))

        # ============================================================
        # REFERENTIAL INTEGRITY CHECK
        # ============================================================

        stored_parent_ids = {parent.parent_id for parent in stored_parents}
        child_parent_ids = {child.parent_id for child in children}
        invalid_parent_ids = child_parent_ids - stored_parent_ids

        print()
        print("=" * 70)
        print("REFERENTIAL INTEGRITY CHECK")
        print("=" * 70)

        print("Stored parent IDs       :", len(stored_parent_ids))
        print("Referenced parent IDs   :", len(child_parent_ids))
        print("Invalid parent references:", invalid_parent_ids)

        # ============================================================
        # CHILD EMBEDDINGS
        # ============================================================

        print()
        print("=" * 70)
        print("CHILD EMBEDDINGS")
        print("=" * 70)

        embedder = EmbeddingService(config.embedding_model_name)
        child_texts = [child.content for child in children]
        child_embeddings = embedder.embed(child_texts)

        print("Children embedded :", len(child_embeddings))
        print("Embedding dimension:", child_embeddings.shape[1])

        # ============================================================
        # QDRANT CHILD PERSISTENCE
        # ============================================================

        print()
        print("=" * 70)
        print("QDRANT CHILD PERSISTENCE")
        print("=" * 70)

        vector_size = embedder.model.get_embedding_dimension()
        vector_store = QdrantVectorStore(
            config=config,
            vector_size=vector_size,
        )

        # vector_store.recreate_collection()

        # vector_store.insert_children(
        #     chunks=children,
        #     embeddings=child_embeddings,
        # )
        vector_store.sync_children(
            document_id=document.document_id,
            chunks=children,
            embeddings=child_embeddings,
        )

        print()
        print("Children written to Qdrant:", len(children))

    finally:
        repository.close()


if __name__ == "__main__":

    main()

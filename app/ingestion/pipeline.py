from typing import List

from pydantic import BaseModel

from app.models.document import Document
from app.models.parent_chunk import ParentChunk
from app.models.child_chunk import ChildChunk

from app.config.settings import (
    ChunkingConfig,
    HybridSearchConfig,
)

from app.chunking.structure_detector import StructureDetector
from app.chunking.structure_aware_parent import (
    StructureAwareParentChunker,
)
from app.chunking.child_chunker import ChildChunker

from app.repositories.parent_repository import ParentRepository

from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sparse_embedding_service import (
    SparseEmbeddingService,
)

from app.vectorstore.hybrid_qdrant_store import (
    HybridQdrantStore,
)

# ============================================================
# INGESTION RESULT
# ============================================================


class IngestionResult(BaseModel):
    """
    Result returned by the ingestion pipeline.

    Keeping parents and children available is useful for:

    - experiments
    - tests
    - diagnostics
    - retrieval comparisons
    """

    parents: List[ParentChunk]
    children: List[ChildChunk]


# ============================================================
# INGESTION PIPELINE
# ============================================================


class StructureAwareRAGDemo:
    """
    Structure-aware Parent/Child ingestion pipeline.

    Flow
    ----
    Document
        -> structure detection
        -> ParentChunk generation
        -> MongoDB parent synchronization
        -> read persisted parents
        -> ChildChunk generation
        -> dense embeddings
        -> sparse BM25 embeddings
        -> hybrid Qdrant storage
    """

    def __init__(
        self,
        config: ChunkingConfig,
        hybrid_config: HybridSearchConfig,
    ):
        self.config = config
        self.hybrid_config = hybrid_config

        # ----------------------------------------------------
        # STRUCTURE
        # ----------------------------------------------------

        self.detector = StructureDetector()
        self.parent_chunker = StructureAwareParentChunker(config)
        self.child_chunker = ChildChunker(config)

        # ----------------------------------------------------
        # PARENT PERSISTENCE
        # ----------------------------------------------------

        self.parent_repository = ParentRepository(config)

        # ----------------------------------------------------
        # DENSE EMBEDDINGS
        # ----------------------------------------------------

        self.dense_embedder = EmbeddingService(config.embedding_model_name)

        # ----------------------------------------------------
        # SPARSE EMBEDDINGS
        # ----------------------------------------------------

        self.sparse_embedder = SparseEmbeddingService(
            model_name=(hybrid_config.sparse_model_name)
        )

        # ----------------------------------------------------
        # HYBRID VECTOR STORE
        # ----------------------------------------------------

        vector_size = self.dense_embedder.model.get_embedding_dimension()

        self.hybrid_vector_store = HybridQdrantStore(
            config=hybrid_config,
            vector_size=vector_size,
            url=(f"http://" f"{config.qdrant_host}:" f"{config.qdrant_port}"),
        )

    # ========================================================
    # INGEST
    # ========================================================

    def ingest(
        self,
        document: Document,
        recreate_hybrid_collection: bool = False,
    ) -> IngestionResult:

        # ====================================================
        # 1. STRUCTURE DETECTION
        # ====================================================

        print()
        print("=" * 70)
        print("STRUCTURE DETECTION")
        print("=" * 70)

        elements = self.detector.detect(document)
        print("Structural elements:", len(elements))

        # ====================================================
        # 2. GENERATE FRESH PARENTS
        # ====================================================

        print()
        print("=" * 70)
        print("STRUCTURE-AWARE PARENT CHUNKING")
        print("=" * 70)

        generated_parents = self.parent_chunker.chunk(
            document=document,
            elements=elements,
        )

        print("Generated parents:", len(generated_parents))

        # ====================================================
        # 3. SYNCHRONIZE PARENTS IN MONGODB
        # ====================================================

        print()
        print("=" * 70)
        print("MONGODB PARENT SYNCHRONIZATION")
        print("=" * 70)

        self.parent_repository.ping()

        sync_result = self.parent_repository.sync_parents(
            document_id=document.document_id,
            parents=generated_parents,
        )

        print("Incoming parents      :", sync_result.incoming_count)
        print("Existing before sync  :", sync_result.existing_count_before)
        print("New parents inserted  :", sync_result.inserted_count)
        print("Unchanged parents     :", sync_result.unchanged_count)
        print("Stale parents deleted :", sync_result.deleted_stale_count)

        print(
            "Parents after sync    :",
            sync_result.final_count,
        )

        # ====================================================
        # 4. READ PERSISTED PARENTS BACK
        # ====================================================

        persisted_parents = self.parent_repository.get_by_document_id(
            document.document_id
        )

        print(
            "Persisted parents read:",
            len(persisted_parents),
        )

        # ====================================================
        # WHY READ THEM BACK?
        # ====================================================
        #
        # ChildChunks MUST reference the parent IDs that are
        # actually persisted in MongoDB.
        #
        # We therefore do NOT create children directly from
        # generated_parents.
        #
        # ====================================================

        # ====================================================
        # 5. CHILD CHUNKING
        # ====================================================

        print()
        print("=" * 70)
        print("CHILD CHUNKING")
        print("=" * 70)

        children = self.child_chunker.chunk_parents(persisted_parents)

        print(
            "Children generated:",
            len(children),
        )

        # ====================================================
        # 6. REFERENTIAL INTEGRITY
        # ====================================================

        persisted_parent_ids = {parent.parent_id for parent in persisted_parents}
        child_parent_ids = {child.parent_id for child in children}
        invalid_parent_ids = child_parent_ids - persisted_parent_ids

        if invalid_parent_ids:
            raise RuntimeError(
                "ChildChunks contain invalid "
                "parent references: "
                f"{invalid_parent_ids}"
            )

        print(
            "Parent references valid:",
            True,
        )

        # ====================================================
        # 7. PREPARE CHILD TEXT
        # ====================================================

        child_texts = [child.content for child in children]

        # ====================================================
        # 8. DENSE EMBEDDINGS
        # ====================================================

        print()
        print("=" * 70)
        print("DENSE CHILD EMBEDDINGS")
        print("=" * 70)

        dense_embeddings = self.dense_embedder.embed_documents(child_texts)

        print(
            "Dense embeddings:",
            len(dense_embeddings),
        )

        if dense_embeddings:
            print(
                "Dense dimension:",
                len(dense_embeddings[0]),
            )

        # ====================================================
        # 9. SPARSE EMBEDDINGS
        # ====================================================

        print()
        print("=" * 70)
        print("SPARSE CHILD EMBEDDINGS")
        print("=" * 70)

        sparse_embeddings = self.sparse_embedder.embed_documents(child_texts)

        print(
            "Sparse embeddings:",
            len(sparse_embeddings),
        )

        # ====================================================
        # 10. HYBRID QDRANT COLLECTION
        # ====================================================

        print()
        print("=" * 70)
        print("HYBRID QDRANT")
        print("=" * 70)

        if recreate_hybrid_collection:

            self.hybrid_vector_store.recreate_collection()

        # ====================================================
        # 11. INSERT CHILDREN
        # ====================================================

        self.hybrid_vector_store.insert_children(
            children=children,
            dense_embeddings=dense_embeddings,
            sparse_embeddings=sparse_embeddings,
        )

        print(
            "Hybrid child points written:",
            len(children),
        )

        # ====================================================
        # 12. RETURN INGESTION RESULT
        # ====================================================

        return IngestionResult(
            parents=persisted_parents,
            children=children,
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(
        self,
    ) -> None:

        self.parent_repository.close()

from typing import Dict, List

from pydantic import BaseModel, Field

from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import EmbeddingService
from app.models.parent_chunk import ParentChunk
from app.repositories.parent_repository import ParentRepository
from app.retrieval.mmr_retriever import (
    MMRCandidate,
    MMRRetriever,
)
from app.vectorstore.qdrant_store import QdrantVectorStore

# ============================================================
# MMR CHILD HIT
# ============================================================


class MMRChildHit(BaseModel):

    child_id: str
    parent_id: str
    document_id: str
    child_index: int

    content: str

    query_similarity: float

    mmr_rank: int
    mmr_score: float

    max_redundancy: float


# ============================================================
# MMR PARENT RESULT
# ============================================================


class MMRParentResult(BaseModel):

    parent: ParentChunk

    first_mmr_rank: int

    best_query_similarity: float

    matched_children: List[MMRChildHit] = Field(default_factory=list)


# ============================================================
# MMR PARENT / CHILD RETRIEVER
# ============================================================


class MMRParentChildRetriever:

    def __init__(
        self,
        config: ChunkingConfig,
        embedder: EmbeddingService,
        vector_store: QdrantVectorStore,
        parent_repository: ParentRepository,
        lambda_mult: float = 0.7,
    ) -> None:

        self.config = config
        self.embedder = embedder
        self.vector_store = vector_store
        self.parent_repository = parent_repository

        self.mmr = MMRRetriever(lambda_mult=lambda_mult)

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        fetch_k: int = 10,
        mmr_child_top_k: int = 5,
        parent_top_k: int = 3,
    ) -> List[MMRParentResult]:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if fetch_k <= 0:
            raise ValueError("fetch_k must be greater than zero.")

        if mmr_child_top_k <= 0:
            raise ValueError("mmr_child_top_k must be greater than zero.")

        if parent_top_k <= 0:
            raise ValueError("parent_top_k must be greater than zero.")

        if mmr_child_top_k > fetch_k:
            raise ValueError("mmr_child_top_k cannot exceed fetch_k.")

        # ====================================================
        # 1. QUERY EMBEDDING
        # ====================================================

        query_vector = self.embedder.embed_query(query)

        # ====================================================
        # 2. FETCH BROAD CHILD CANDIDATE POOL FROM QDRANT
        #
        # IMPORTANT:
        # We request the stored vectors because MMR needs
        # candidate-to-candidate similarity.
        # ====================================================

        qdrant_hits = self.vector_store.search(
            query_vector=query_vector,
            top_k=fetch_k,
            with_vectors=True,
        )

        # ====================================================
        # 3. CONVERT QDRANT HITS INTO MMR CANDIDATES
        # ====================================================

        candidates: List[MMRCandidate] = []

        for hit in qdrant_hits:

            payload = hit.payload or {}

            parent_id = payload.get("parent_id")

            if not parent_id:
                raise RuntimeError(
                    "Qdrant child payload is missing "
                    "'parent_id'. "
                    f"Point ID: {hit.id}"
                )

            if hit.vector is None:
                raise RuntimeError(
                    "MMR retrieval requires stored "
                    "Qdrant vectors, but vector was "
                    f"missing for point {hit.id}."
                )

            vector = [float(value) for value in hit.vector]

            candidates.append(
                MMRCandidate(
                    id=payload.get(
                        "child_id",
                        str(hit.id),
                    ),
                    content=payload.get(
                        "content",
                        "",
                    ),
                    query_similarity=float(hit.score),
                    embedding=vector,
                    metadata={
                        "parent_id": parent_id,
                        "document_id": payload.get(
                            "document_id",
                            "",
                        ),
                        "child_index": payload.get(
                            "child_index",
                            -1,
                        ),
                    },
                )
            )

        # ====================================================
        # 4. MMR SELECTS DIVERSE CHILDREN
        # ====================================================

        mmr_results = self.mmr.select(
            candidates=candidates,
            top_k=mmr_child_top_k,
        )

        # ====================================================
        # 5. GROUP SELECTED CHILDREN BY PARENT
        # ====================================================

        children_by_parent: Dict[
            str,
            List[MMRChildHit],
        ] = {}

        for result in mmr_results:

            parent_id = result.metadata["parent_id"]

            child_hit = MMRChildHit(
                child_id=result.id,
                parent_id=parent_id,
                document_id=(result.metadata["document_id"]),
                child_index=(result.metadata["child_index"]),
                content=result.content,
                query_similarity=(result.query_similarity),
                mmr_rank=result.rank,
                mmr_score=result.mmr_score,
                max_redundancy=(result.max_redundancy),
            )

            children_by_parent.setdefault(
                parent_id,
                [],
            ).append(child_hit)

        # ====================================================
        # 6. EXPAND UNIQUE PARENTS FROM MONGODB
        # ====================================================

        parent_results: List[MMRParentResult] = []

        for (
            parent_id,
            child_hits,
        ) in children_by_parent.items():

            parent = self.parent_repository.get_by_id(parent_id)

            if parent is None:
                raise RuntimeError(
                    "Dangling ChildChunk reference "
                    "detected. "
                    f"parent_id={parent_id} "
                    "does not exist in MongoDB."
                )

            child_hits.sort(key=lambda child: child.mmr_rank)

            first_mmr_rank = min(child.mmr_rank for child in child_hits)

            best_query_similarity = max(child.query_similarity for child in child_hits)

            parent_results.append(
                MMRParentResult(
                    parent=parent,
                    first_mmr_rank=(first_mmr_rank),
                    best_query_similarity=(best_query_similarity),
                    matched_children=(child_hits),
                )
            )

        # ====================================================
        # 7. PARENT ORDER FOLLOWS EARLIEST MMR CHILD
        # ====================================================

        parent_results.sort(key=lambda result: result.first_mmr_rank)

        return parent_results[:parent_top_k]

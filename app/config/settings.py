from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================


class ChunkingConfig(BaseModel):

    # --------------------------------------------------------
    # CHUNKING
    # --------------------------------------------------------

    max_chunk_chars: int = 300
    min_chunk_chars: int = 100

    # --------------------------------------------------------
    # CHILD CHUNKING
    # --------------------------------------------------------

    child_chunk_chars: int = 120
    child_overlap_chars: int = 30

    # --------------------------------------------------------
    # EMBEDDING
    # --------------------------------------------------------

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --------------------------------------------------------
    # QDRANT - LEGACY DENSE COLLECTION
    # --------------------------------------------------------

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    collection_name: str = "structure_aware_v4_benchmark_v2"

    top_k: int = 3

    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    child_top_k: int = 5
    child_score_threshold: float = 0.40
    parent_top_k: int = 2

    # --------------------------------------------------------
    # MONGODB
    # --------------------------------------------------------

    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb://localhost:27017",
    )

    mongodb_uri: str = MONGODB_URI
    mongodb_database: str = "agentic_rag"

    # IMPORTANT:
    # V2 benchmark gets its own collection.
    mongodb_parent_collection: str = "parents_benchmark_v2"

    # --------------------------------------------------------
    # VERSIONING
    # --------------------------------------------------------

    ingestion_version: str = "benchmark_v2"
    parent_chunking_version: str = "parent_v2"
    child_chunking_version: str = "child_v2"


class HybridSearchConfig(BaseModel):

    # --------------------------------------------------------
    # BENCHMARK V2 HYBRID COLLECTION
    # --------------------------------------------------------

    collection_name: str = "structure_aware_v4_benchmark_v2"
    dense_vector_name: str = "dense"
    sparse_vector_name: str = "sparse"
    sparse_model_name: str = "Qdrant/bm25"
    dense_prefetch_k: int = Field(
        default=15,
        ge=1,
    )
    sparse_prefetch_k: int = Field(
        default=15,
        ge=1,
    )
    final_k: int = Field(
        default=10,
        ge=1,
    )

    rrf_k: int = Field(
        default=2,
        ge=1,
    )

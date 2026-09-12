from app.models.document import Document

# ============================================================
# DEMO DOCUMENT
# ============================================================


class DemoDocumentFactory:

    @staticmethod
    def create() -> Document:

        text = """
# Vector Databases

Vector databases are designed to store and retrieve high-dimensional vectors.

They are commonly used in semantic search and Retrieval Augmented Generation systems.

A vector database allows applications to find information based on semantic similarity rather than exact keyword matching.

## Qdrant

Qdrant is a vector database designed for similarity search.

It stores vectors together with payload metadata.

Applications can use payload metadata to filter search results.

Qdrant is commonly used in modern RAG systems because it combines vector similarity search with metadata filtering.

## HNSW

HNSW is an approximate nearest neighbor indexing algorithm.

It builds a graph structure that allows vectors to be searched efficiently.

The graph contains multiple layers.

Higher layers provide long-range connections while lower layers provide more detailed navigation.

During search, the algorithm starts at an upper layer and progressively moves toward lower layers.

This allows the search to avoid comparing the query with every vector in the database.

### M Parameter

The M parameter has control over the number of connections maintained by each node.

Increasing M can improve recall but also increases memory consumption and indexing cost.

### ef_construct

The ef_construct parameter controls how broadly the graph is explored during index construction.

A higher ef_construct value can improve graph quality but increases index construction time.

## Metadata

Metadata provides addl information about a document or chunk.

Examples include document ID, source, section name, page number, content type, and creation date.

Metadata can be stored alongside vectors and used for filtering during retrieval.
"""

        return Document(
            document_id="vector-db-demo-001",
            source="vector-database-guide.md",
            text=text,
        )

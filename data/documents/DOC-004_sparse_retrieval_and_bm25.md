# Sparse Retrieval and BM25

Document ID: DOC-004

## Lexical

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and document length.

## Identifiers

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong sparse-search signals.

## Limit

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to the same concept without sharing the same terms.

## Role

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical precision.


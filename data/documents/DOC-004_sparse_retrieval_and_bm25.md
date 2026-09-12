# Sparse Retrieval and BM25

Document ID: DOC-004

## Lexical

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and document length.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Identifiers

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong sparse-search signals.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Limit

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to the same concept without sharing the same terms.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Role

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical precision.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

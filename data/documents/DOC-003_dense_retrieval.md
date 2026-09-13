# Dense Retrieval

Document ID: DOC-003

## Semantics

Dense retrieval embeds queries and documents into vectors so semantically related text can match despite different wording. A query about making index construction more thorough can retrieve a passage about increasing ef_construct.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Cosine

Cosine similarity measures geometric similarity, not the probability that a passage answers the question. Semantically related but non-answering passages can receive high scores.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Weaknesses

Opaque identifiers, error codes, version strings, and rare names such as uq_document_content_hash or ERR_CONNECTION_REFUSED can be difficult for a dense model.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Breadth

Candidate top_k controls recall opportunity. A later reranker cannot recover a relevant document that was removed before reranking.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

# Dense Retrieval

Document ID: DOC-003

## Semantics

Dense retrieval embeds queries and documents into vectors so semantically related text can match despite different wording. A query about making index construction more thorough can retrieve a passage about increasing ef_construct.

## Cosine

Cosine similarity measures geometric similarity, not the probability that a passage answers the question. Semantically related but non-answering passages can receive high scores.

## Weaknesses

Opaque identifiers, error codes, version strings, and rare names such as uq_document_content_hash or ERR_CONNECTION_REFUSED can be difficult for a dense model.

## Breadth

Candidate top_k controls recall opportunity. A later reranker cannot recover a relevant document that was removed before reranking.


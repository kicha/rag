# Vector Search Failure Modes

Document ID: DOC-023

## Dimensions

A collection configured for 384-dimensional vectors cannot accept 768-dimensional vectors. Model migrations often expose this error.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Duplicates

Repeated ingestion creates duplicates if logical chunks receive new random point identities and no synchronization reconciles them.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Recall

Low recall can result from poor chunking, weak embeddings, small candidate pools, restrictive filters, HNSW settings, or missing source content.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Scores

High cosine similarity means semantic relatedness, not guaranteed answer correctness; low CrossEncoder output may also reflect query phrasing.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

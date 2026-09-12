# Retrieval Observability

Document ID: DOC-021

## Stages

Trace dense, sparse, RRF fusion, parent expansion, CrossEncoder, MMR, and final context separately.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Scores

An RRF score, cosine similarity, BM25 score, and CrossEncoder output have different meanings and should not be logged under an unlabeled generic score.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Latency

Measure embedding, dense search, sparse search, fusion, MongoDB lookup, reranker inference, and MMR latency separately.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Diagnosis

Stage-level traces reveal whether bad answers came from candidate recall, stale parent links, reranking, diversity selection, or generation.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

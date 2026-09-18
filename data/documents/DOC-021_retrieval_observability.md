# Retrieval Observability

Document ID: DOC-021

## Stages

Trace dense, sparse, RRF fusion, parent expansion, CrossEncoder, MMR, and final context separately.

## Scores

An RRF score, cosine similarity, BM25 score, and CrossEncoder output have different meanings and should not be logged under an unlabeled generic score.

## Latency

Measure embedding, dense search, sparse search, fusion, MongoDB lookup, reranker inference, and MMR latency separately.

## Diagnosis

Stage-level traces reveal whether bad answers came from candidate recall, stale parent links, reranking, diversity selection, or generation.


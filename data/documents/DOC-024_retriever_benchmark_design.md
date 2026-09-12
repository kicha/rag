# Retriever Benchmark Design

Document ID: DOC-024

## Corpus

A useful benchmark is large enough that top_k cannot expose almost the whole collection. It should include overlapping topics, near-duplicates, exact identifiers, paraphrases, and plausible distractors.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Queries

Include lexical queries like ef_construct and HTTP 422, semantic paraphrases, composite questions, and unanswerable requests.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Compare

Run Dense, Sparse, Hybrid, Hybrid plus CrossEncoder, and Hybrid plus CrossEncoder plus Parent MMR against the same corpus and labels.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Report

Report Recall@5, Recall@10, MRR, candidate parent recall, final context precision, and latency.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

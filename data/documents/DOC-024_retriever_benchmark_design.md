# Retriever Benchmark Design

Document ID: DOC-024

## Corpus

A useful benchmark is large enough that top_k cannot expose almost the whole collection. It should include overlapping topics, near-duplicates, exact identifiers, paraphrases, and plausible distractors.

## Queries

Include lexical queries like ef_construct and HTTP 422, semantic paraphrases, composite questions, and unanswerable requests.

## Compare

Run Dense, Sparse, Hybrid, Hybrid plus CrossEncoder, and Hybrid plus CrossEncoder plus Parent MMR against the same corpus and labels.

## Report

Report Recall@5, Recall@10, MRR, candidate parent recall, final context precision, and latency.


# Agentic RAG Moderate Retrieval Corpus

Original controlled benchmark for Dense, Sparse/BM25, Hybrid RRF, CrossEncoder,
Parent/Child retrieval, and Parent MMR.

Contents:
- 24 Markdown technical documents
- 32 labeled queries in gold_queries.json
- manifest.json with approximate corpus size

The corpus deliberately includes overlapping concepts, exact identifiers,
paraphrasable questions, distractors, failure modes, and one unanswerable query.

Recommended use:
1. Ingest each DOC-*.md as a separate Document preserving its Document ID.
2. Run the existing structure-aware parent/child pipeline.
3. Compare Dense, Sparse, Hybrid, Hybrid->CrossEncoder, and
   Hybrid->CrossEncoder->Parent MMR.
4. Measure Recall@5, Recall@10, MRR, candidate-parent recall, precision, latency.

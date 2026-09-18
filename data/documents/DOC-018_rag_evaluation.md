# RAG Evaluation

Document ID: DOC-018

## Metrics

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

## Parents

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall before reranking is especially important.

## Answer

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and citation correctness are separate concerns.

## Gold

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs, and unanswerable queries.


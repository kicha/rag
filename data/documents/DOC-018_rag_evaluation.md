# RAG Evaluation

Document ID: DOC-018

## Metrics

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Parents

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall before reranking is especially important.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Answer

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and citation correctness are separate concerns.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Gold

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs, and unanswerable queries.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

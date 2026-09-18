# Multi Query Retrieval

Document ID: DOC-016

## Views

Multi-query retrieval generates several search formulations from one user request, retrieves for each, then merges and deduplicates candidates.

## Recall

Different phrasings can recover evidence using terms such as graph traversal, approximate neighbors, upper layers, or search frontier.

## Cost

Every generated query adds embedding, vector search, sparse search, and possibly reranking work.

## Fusion

Multi-query results can be merged with rank fusion, maximum score, or another rule; noisy generated queries can otherwise promote distractors.


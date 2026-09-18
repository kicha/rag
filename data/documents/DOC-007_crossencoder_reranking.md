# CrossEncoder Reranking

Document ID: DOC-007

## Scoring

A CrossEncoder jointly processes query and candidate text, allowing deeper query-document interaction than independent embeddings.

## Placement

CrossEncoder reranking follows broad first-stage retrieval because pairwise inference is more expensive. Missing candidates cannot be recovered.

## Calibration

CrossEncoder outputs should not automatically be treated as universally calibrated probabilities. Query phrasing can change scores substantially.

## Parents

In parent child RAG, a useful pattern retrieves children, expands parents, then reranks full ParentChunk content.


# Vector Search Failure Modes

Document ID: DOC-023

## Dimensions

A collection configured for 384-dimensional vectors cannot accept 768-dimensional vectors. Model migrations often expose this error.

## Duplicates

Repeated ingestion creates duplicates if logical chunks receive new random point identities and no synchronization reconciles them.

## Recall

Low recall can result from poor chunking, weak embeddings, small candidate pools, restrictive filters, HNSW settings, or missing source content.

## Scores

High cosine similarity means semantic relatedness, not guaranteed answer correctness; low CrossEncoder output may also reflect query phrasing.


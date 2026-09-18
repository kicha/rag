# Qdrant Named Vectors

Document ID: DOC-011

## Points

A Qdrant point can contain an identifier, payload metadata, and one or more vector representations.

## Names

A hybrid point can store a dense vector named dense and a sparse vector named sparse while sharing the same ChildChunk payload.

## Sparse

Sparse vector indices are lexical features, not positions inside a 384-dimensional MiniLM vector.

## Upsert

Stable point identity matters for idempotent ingestion. Recreating a collection is convenient for experiments but is not a final synchronization design.


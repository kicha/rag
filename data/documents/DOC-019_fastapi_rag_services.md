# FastAPI RAG Services

Document ID: DOC-019

## API

A RAG service may expose POST /query, POST /ingest, GET /health, and document endpoints using Pydantic request and response models.

## HTTP 422

FastAPI commonly returns HTTP 422 when request data fails validation against the declared schema. This is an API validation failure, not a retrieval-quality failure.

## Boundaries

Embedding services, repositories, vector stores, retrievers, and rerankers should be initialized through clear application boundaries.

## Trace

Request IDs, retrieval timings, candidate counts, and final document IDs are useful production signals.


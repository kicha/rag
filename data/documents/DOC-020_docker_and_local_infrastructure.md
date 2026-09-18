# Docker and Local Infrastructure

Document ID: DOC-020

## Services

A local stack can run Qdrant, MongoDB, and the Python API as separate services with explicit ports and health checks.

## Refused

ERR_CONNECTION_REFUSED usually means the target service is not listening, a container is stopped, the host or port is wrong, or networking is misconfigured.

## Persistence

Persistent volumes preserve Qdrant and MongoDB data across container recreation.

## Config

Environment variables should hold service URLs and credentials while local defaults may use http://localhost:6333 for Qdrant.


# Embeddings and Normalization

Document ID: DOC-014

## Model

all-MiniLM-L6-v2 is a lightweight sentence-transformer baseline that produces 384-dimensional dense embeddings.

## Normalize

Unit-normalized vectors make cosine similarity equivalent to dot product. Query and document preprocessing should be consistent.

## Migration

Changing to a model with another dimensionality requires regenerating vectors and using a compatible collection configuration.

## Domain

Generic semantic quality does not guarantee strong handling of product identifiers, uncommon acronyms, or error strings.


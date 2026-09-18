# MongoDB Parent Repository

Document ID: DOC-013

## Store

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

## Indexes

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting existing index options can produce IndexOptionsConflict.

## Sync

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based on content hashes.

## Lookup

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is missing.


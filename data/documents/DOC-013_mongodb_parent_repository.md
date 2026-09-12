# MongoDB Parent Repository

Document ID: DOC-013

## Store

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Indexes

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting existing index options can produce IndexOptionsConflict.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Sync

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based on content hashes.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Lookup

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is missing.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

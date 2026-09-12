# Qdrant Synchronization

Document ID: DOC-012

## Idempotency

Repeated ingestion of unchanged source content should not create duplicate logical child points.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Coarse sync

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Differential

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Dangling

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this integrity failure.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

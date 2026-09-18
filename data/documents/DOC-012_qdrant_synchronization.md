# Qdrant Synchronization

Document ID: DOC-012

## Idempotency

Repeated ingestion of unchanged source content should not create duplicate logical child points.

## Coarse sync

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

## Differential

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

## Dangling

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this integrity failure.


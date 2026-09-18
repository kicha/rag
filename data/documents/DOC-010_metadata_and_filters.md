# Metadata and Filters

Document ID: DOC-010

## Schema

Useful metadata includes document_id, source, version, page_number, language, section_path, heading levels, content_type, tenant_id, and timestamps.

## Filtering

Authorization fields such as tenant_id should filter before semantic ranking when cross-tenant leakage is unacceptable.

## Indexes

Frequently filtered metadata may need payload indexes. Indexing every field wastes resources and increases write overhead.

## Debug

Document identity, parent_id, child_index, section path, and source location make retrieval results explainable.


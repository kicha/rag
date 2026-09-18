# Tenant Isolation

Document ID: DOC-022

## Tenant

tenant_id should be a retrieval constraint when tenants must not access one another's documents.

## Permissions

Access rules may also use source_id, project_id, category, or group metadata with consistent types and index support.

## Security

Semantic relevance can never override authorization. Permission filtering and retrieval ranking solve different problems.

## Test

Negative tests should prove that tenant A cannot retrieve tenant B content even if their text is nearly identical.


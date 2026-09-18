# Parent Child Retrieval

Document ID: DOC-006

## Purpose

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

## Identity

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create dangling references if persisted IDs differ.

## Dedup

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while retaining matched-child evidence for debugging.

## Trade-off

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller than the best generation context unit.


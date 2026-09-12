# Parent Child Retrieval

Document ID: DOC-006

## Purpose

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Identity

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create dangling references if persisted IDs differ.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Dedup

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while retaining matched-child evidence for debugging.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Trade-off

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller than the best generation context unit.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

# Query Rewriting

Document ID: DOC-015

## Purpose

Query rewriting changes wording to better match corpus terminology while trying to preserve the original intent.

## Example

How does HNSW search efficiently can be rewritten toward graph traversal, upper-to-lower layers, and avoiding comparison with every vector.

## Risk

A rewriter can introduce assumptions or drift. Systems should retain the original query and may retrieve with both forms.

## Measure

Judge rewriting with downstream retrieval metrics rather than linguistic elegance.


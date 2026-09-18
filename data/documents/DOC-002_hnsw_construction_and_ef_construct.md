# HNSW Construction and ef_construct

Document ID: DOC-002

## Meaning

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality graph.

## Trade-off

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M, and ef_search all interact.

## Example

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or one hundred edges.

## Rebuild

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the change can influence graph quality.


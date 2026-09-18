# HNSW Architecture and Search

Document ID: DOC-001

## Layers

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

## M parameter

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

## ef_search

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

## Tuning

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.


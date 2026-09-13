# HNSW Architecture and Search

Document ID: DOC-001

## Layers

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## M parameter

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## ef_search

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Tuning

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

# Chunking Strategies

Document ID: DOC-009

## Fixed

Fixed character chunks are simple but can split semantic units. Recursive chunking tries paragraph, sentence, and whitespace boundaries before smaller fallbacks.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Semantic

Semantic chunking uses embedding distance between neighboring units and can choose breakpoints from percentile, standard-deviation, IQR, or gradient rules.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Structure

Structure-aware chunking preserves headings, lists, code blocks, and hierarchy such as Vector Databases > HNSW > ef_construct.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Evaluation

Chunking choices should be compared with retrieval recall, answer quality, chunk count, ingestion cost, and boundary quality.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

# Chunking Strategies

Document ID: DOC-009

## Fixed

Fixed character chunks are simple but can split semantic units. Recursive chunking tries paragraph, sentence, and whitespace boundaries before smaller fallbacks.

## Semantic

Semantic chunking uses embedding distance between neighboring units and can choose breakpoints from percentile, standard-deviation, IQR, or gradient rules.

## Structure

Structure-aware chunking preserves headings, lists, code blocks, and hierarchy such as Vector Databases > HNSW > ef_construct.

## Evaluation

Chunking choices should be compared with retrieval recall, answer quality, chunk count, ingestion cost, and boundary quality.


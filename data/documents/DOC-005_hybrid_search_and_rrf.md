# Hybrid Search and RRF

Document ID: DOC-005

## Hybrid

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## RRF

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Prefetch

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Caveat

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw score gap was between adjacent candidates.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

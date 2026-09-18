# Hybrid Search and RRF

Document ID: DOC-005

## Hybrid

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

## RRF

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

## Prefetch

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

## Caveat

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw score gap was between adjacent candidates.


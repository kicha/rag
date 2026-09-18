# Maximal Marginal Relevance

Document ID: DOC-008

## Formula

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times relevance minus one minus lambda times maximum redundancy.

## Lambda

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual yet weakly relevant items.

## Space

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

## Pipeline

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.


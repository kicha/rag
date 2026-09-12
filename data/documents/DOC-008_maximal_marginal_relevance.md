# Maximal Marginal Relevance

Document ID: DOC-008

## Formula

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times relevance minus one minus lambda times maximum redundancy.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Lambda

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual yet weakly relevant items.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Space

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

## Pipeline

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.

Operationally, this topic should be validated with reproducible experiments rather than a single example. Record configuration, candidate counts, ranking order, identifiers, latency, and failure cases. Similar vocabulary can appear in neighboring retrieval topics, so evaluation should reward the most directly relevant document rather than any document that merely shares technical words.

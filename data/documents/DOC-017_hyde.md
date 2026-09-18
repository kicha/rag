# HyDE

Document ID: DOC-017

## Idea

Hypothetical Document Embeddings generate an answer-like hypothetical passage, embed it, and use that embedding for retrieval.

## Bridge

The hypothetical passage may introduce terminology closer to the corpus than the original short question.

## Risk

The hypothetical document may hallucinate. It is only a retrieval aid and must never replace source evidence.

## Measure

Compare HyDE against original-query retrieval because its extra generation step adds cost and is not universally beneficial.


import numpy as np


def cosine_similarity(v1, v2):
    """Calculates the cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


def maximal_marginal_relevance(query_embedding, doc_embeddings, lambda_param=0.5, k=2):
    """
    Selects the top-k diverse and relevant documents using the MMR algorithm.
    """
    # 1. Calculate similarity of all documents to the user query (Relevance)
    query_similarities = [
        cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings
    ]
    print(f"Query Similarities: {query_similarities}")
    unselected_indices = list(range(len(doc_embeddings)))
    selected_indices = []
    print(f"Unselected Indices: {unselected_indices}")
    # 2. Pick the first document automatically (highest similarity to query)
    first_pick = np.argmax(query_similarities)
    selected_indices.append(first_pick)
    unselected_indices.remove(first_pick)
    print(
        f"First Pick Index: {first_pick}, Similarity: {query_similarities[first_pick]}"
    )

    # 3. Iteratively calculate MMR scores for the remaining pool
    while len(selected_indices) < k and unselected_indices:
        print(f"Current Selected Indices: {selected_indices}")
        mmr_scores = []

        for idx in unselected_indices:
            print(f"Evaluating Candidate Index: {idx}")
            relevance = query_similarities[idx]
            print(f"Evaluating Index: {idx}, Relevance: {relevance}")
            # Find the max similarity between this candidate and all already selected documents
            redundancy = max(
                [
                    cosine_similarity(doc_embeddings[idx], doc_embeddings[sel_idx])
                    for sel_idx in selected_indices
                ]
            )
            print(f"Redundancy for Index {idx}: {redundancy}")
            # The MMR Equation
            score = (lambda_param * relevance) - ((1 - lambda_param) * redundancy)
            mmr_scores.append((score, idx))

        # Select the index with the absolute highest MMR score
        best_score, best_idx = max(mmr_scores, key=lambda x: x[0])
        selected_indices.append(best_idx)
        unselected_indices.remove(best_idx)
        print(f"Selected Index: {best_idx}, MMR Score: {best_score}")

    return selected_indices


# --- Example Usage ---
if __name__ == "__main__":
    # Documents text representation for context:
    # doc_0: "The Pyramids were grand tombs for Egyptian pharaohs."
    # doc_1: "Pharaohs were buried in the Egyptian Pyramids." (Duplicate of doc_0)
    # doc_2: "The Great Sphinx stands guard near the pyramids." (Diverse but relevant)
    # doc_3: "Machu Picchu is located high in the Andes." (Irrelevant)

    # Simplified mock embeddings (dimensions map to concepts: [Pyramids, Pharaohs, Sphinx, Peru])
    query_vector = np.array([1.0, 1.0, 0.5, 0.0])

    doc_vectors = [
        np.array([1.0, 1.0, 0.0, 0.0]),  # Doc 0: Highly relevant
        np.array([0.9, 0.9, 0.0, 0.0]),  # Doc 1: Highly relevant but identical to Doc 0
        np.array(
            [0.5, 0.0, 1.0, 0.0]
        ),  # Doc 2: Relevant and introduces new info (Sphinx)
        np.array([0.0, 0.0, 0.0, 1.0]),  # Doc 3: Completely irrelevant
    ]

    # Run MMR to fetch the top 2 best results
    chosen_indices = maximal_marginal_relevance(
        query_vector, doc_vectors, lambda_param=0.5, k=2
    )

    print(f"Selected Document Indices: {chosen_indices}")
    # Output will be [0, 2] instead of [0, 1] because Doc 1 is too redundant!

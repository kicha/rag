from app.config.settings import ChunkingConfig
from app.embeddings.embedding_service import EmbeddingService
from app.repositories.parent_repository import ParentRepository
from app.retrieval.mmr_parent_child_retriever import MMRParentChildRetriever
from app.retrieval.parent_child_retriever import ParentChildRetriever
from app.reranking.cross_encoder_reranker import CrossEncoderReranker
from app.vectorstore.qdrant_store import QdrantVectorStore
from app.retrieval.mmr_rerank_retriever import MMRRerankRetriever
from app.retrieval.rerank_mmr_retriever import RerankMMRRetriever

# ============================================================
# PRINT PLAIN RETRIEVAL
# ============================================================


def print_plain_results(
    results,
) -> None:

    print()
    print("=" * 72)
    print("1. PLAIN SIMILARITY RETRIEVAL")
    print("=" * 72)

    for rank, result in enumerate(results, start=1):
        parent = result.parent
        print()
        print(f"RANK             : {rank}")
        print(f"Best child score : {result.best_score:.4f}")
        print(f"Parent index     : {parent.parent_index}")
        print(f"Section          : {parent.heading_context.get_section_path()}")
        print(f"Matched children : {len(result.matched_children)}")
        print()
        print(parent.content)


# ============================================================
# PRINT MMR
# ============================================================


def print_mmr_results(
    results,
) -> None:

    print()
    print("=" * 72)
    print("2. MMR RETRIEVAL")
    print("=" * 72)

    for rank, result in enumerate(results, start=1):
        parent = result.parent
        print()
        print(f"PARENT RANK           : {rank}")
        print(f"First MMR child rank  : " f"{result.first_mmr_rank}")
        print(f"Best query similarity : " f"{result.best_query_similarity:.4f}")
        print(f"Parent index          : " f"{parent.parent_index}")
        print(
            f"Section               : " f"{parent.heading_context.get_section_path()}"
        )

        for child in result.matched_children:

            print()
            print(f"  MMR child rank  : " f"{child.mmr_rank}")
            print(f"  Query similarity: " f"{child.query_similarity:.4f}")
            print(f"  Max redundancy  : " f"{child.max_redundancy:.4f}")
            print(f"  MMR score       : " f"{child.mmr_score:.4f}")
            print(f"  Content         : " f"{child.content!r}")

        print()
        print("FULL PARENT")
        print("-" * 72)
        print(parent.content)


# ============================================================
# PRINT RERANKED
# ============================================================


def print_reranked_results(
    response,
) -> None:

    print()
    print("=" * 72)
    print("3. CROSS-ENCODER RERANKING")
    print("=" * 72)

    for item in response.results:

        parent = item.result.parent
        print()
        print(f"RERANKED RANK       : " f"{item.reranked_rank}")
        print(f"Original vector rank: " f"{item.original_rank}")
        print(f"Vector score        : " f"{item.vector_score:.4f}")
        print(f"Reranker score      : " f"{item.reranker_score:.4f}")
        print(f"Parent index        : " f"{parent.parent_index}")
        print(f"Section             : " f"{parent.heading_context.get_section_path()}")
        print()
        print(parent.content)


# ============================================================
# APPLICATION
# ============================================================


def main() -> None:

    config = ChunkingConfig()
    embedder = EmbeddingService(config.embedding_model_name)
    vector_size = embedder.model.get_embedding_dimension()
    vector_store = QdrantVectorStore(
        config=config,
        vector_size=vector_size,
    )

    parent_repository = ParentRepository(config=config)

    try:

        query = "How does HNSW search efficiently?"

        print()
        print("=" * 72)
        print("ADVANCED RETRIEVAL COMPARISON")
        print("=" * 72)

        print()
        print(f"QUERY: {query}")

        # ====================================================
        # PLAIN SIMILARITY
        # ====================================================

        plain_retriever = ParentChildRetriever(
            config=config,
            embedder=embedder,
            vector_store=vector_store,
            parent_repository=(parent_repository),
        )

        plain_results = plain_retriever.retrieve(
            query=query,
            child_top_k=10,
            child_score_threshold=0.0,
            parent_top_k=3,
        )

        print_plain_results(plain_results)

        # ====================================================
        # MMR
        # ====================================================

        mmr_retriever = MMRParentChildRetriever(
            config=config,
            embedder=embedder,
            vector_store=vector_store,
            parent_repository=(parent_repository),
            lambda_mult=0.7,
        )

        mmr_results = mmr_retriever.retrieve(
            query=query,
            fetch_k=10,
            mmr_child_top_k=5,
            parent_top_k=3,
        )

        print_mmr_results(mmr_results)

        # ====================================================
        # CROSS-ENCODER
        #
        # IMPORTANT:
        # Give reranker a BROADER candidate set.
        # ====================================================

        rerank_candidates = plain_retriever.retrieve(
            query=query,
            child_top_k=10,
            child_score_threshold=0.0,
            parent_top_k=10,
        )

        reranker = CrossEncoderReranker()

        reranked_response = reranker.rerank(
            query=query,
            candidates=(rerank_candidates),
            top_k=3,
        )

        print_reranked_results(reranked_response)

        # ============================================================
        # MMR + CROSS-ENCODER
        # ============================================================

        combined_retriever = MMRRerankRetriever(
            mmr_retriever=mmr_retriever,
            reranker=reranker,
        )

        # combined_response = combined_retriever.retrieve(
        #     query=query,
        #     fetch_k=10,
        #     mmr_child_top_k=5,
        #     mmr_parent_top_k=5,
        #     reranker_top_k=3,
        # )
        combined_response = combined_retriever.retrieve(
            query=query,
            fetch_k=15,
            mmr_child_top_k=8,
            mmr_parent_top_k=6,
            reranker_top_k=6,
        )

        print()
        print("=" * 72)
        print("4. MMR + CROSS-ENCODER")
        print("=" * 72)

        for item in combined_response.results:
            parent = item.result.parent
            print()
            print(f"FINAL RANK           : " f"{item.reranked_rank}")
            print(f"Best query similarity: " f"{item.vector_score:.4f}")
            print(f"CrossEncoder score   : " f"{item.reranker_score:.4f}")
            print(f"Parent index         : " f"{parent.parent_index}")
            print(
                f"Section              : "
                f"{parent.heading_context.get_section_path()}"
            )
            print()
            print(parent.content)

        # ============================================================
        # CROSS-ENCODER -> PARENT MMR
        # ============================================================

        rerank_mmr_retriever = RerankMMRRetriever(
            parent_child_retriever=(plain_retriever),
            reranker=reranker,
            embedder=embedder,
            lambda_mult=0.7,
        )

        # rerank_mmr_results = rerank_mmr_retriever.retrieve(
        #     query=query,
        #     child_top_k=15,
        #     reranker_candidate_top_k=6,
        #     final_top_k=3,
        # )
        rerank_mmr_results = rerank_mmr_retriever.retrieve(
            query=query,
            child_top_k=15,
            cross_encoder_top_k=5,
            final_top_k=3,
        )

        # print()
        # print("=" * 72)
        # print("5. CROSS-ENCODER + PARENT MMR")
        # print("=" * 72)

        # for result in rerank_mmr_results:
        #     parent = result.parent
        #     print()
        #     print(f"FINAL RANK              : " f"{result.rank}")
        #     print(f"CrossEncoder rank       : " f"{result.reranker_rank}")
        #     print(f"CrossEncoder relevance  : " f"{result.relevance_score:.4f}")
        #     print(f"Max parent redundancy   : " f"{result.max_redundancy:.4f}")
        #     print(f"Relevance contribution  : " f"{result.relevance_contribution:.4f}")
        #     print(f"Redundancy penalty      : " f"{result.redundancy_penalty:.4f}")
        #     print(f"Parent MMR score        : " f"{result.mmr_score:.4f}")
        #     print(f"Parent index            : " f"{parent.parent_index}")
        #     print(
        #         f"Section                 : "
        #         f"{parent.heading_context.get_section_path()}"
        #     )
        #     print()
        #     print(parent.content)

        print()
        print("=" * 72)
        print("5. CROSS-ENCODER PRUNING -> PARENT MMR")
        print("=" * 72)

        for result in rerank_mmr_results:
            parent = result.parent
            print()
            print(f"FINAL RANK              : " f"{result.rank}")
            print(f"CrossEncoder rank       : " f"{result.cross_encoder_rank}")
            print(f"CrossEncoder score      : " f"{result.cross_encoder_score:.4f}")
            print(f"Dense query similarity  : " f"{result.query_similarity:.4f}")
            print(f"Max parent redundancy   : " f"{result.max_redundancy:.4f}")
            print(f"Relevance contribution  : " f"{result.relevance_contribution:.4f}")
            print(f"Redundancy penalty      : " f"{result.redundancy_penalty:.4f}")
            print(f"Parent MMR score        : " f"{result.mmr_score:.4f}")
            print(f"Parent index            : " f"{parent.parent_index}")
            print(
                f"Section                 : "
                f"{parent.heading_context.get_section_path()}"
            )
            print()
            print(parent.content)

    finally:

        parent_repository.close()


if __name__ == "__main__":
    main()

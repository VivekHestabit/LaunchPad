import hashlib
from typing import List, Dict

from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.pipelines.mmr import MMRSelector


class ContextBuilder:

    def __init__(self, max_tokens=1200):
        self.max_tokens = max_tokens
        self.mmr = MMRSelector()

    def _hash_text(self, text: str) -> str:
        return hashlib.md5(text.strip().encode("utf-8")).hexdigest()

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text.split()) * 1.3)

    def deduplicate(self, chunks: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []

        for chunk in chunks:
            text_hash = self._hash_text(chunk["text"])
            if text_hash not in seen:
                seen.add(text_hash)
                unique.append(chunk)

        return unique

    def build_context(self, reranked_chunks: List[Dict], top_k=5) -> Dict:

        reranked_chunks = self.deduplicate(reranked_chunks)

        selected_chunks = self.mmr.select(
            reranked_chunks,
            top_k
        )

        context_blocks = []
        sources = []
        token_count = 0

        for idx, chunk in enumerate(selected_chunks):

            tokens = self._estimate_tokens(chunk["text"])
            if token_count + tokens > self.max_tokens:
                break

            source_id = f"[SOURCE {idx + 1}]"

            context_blocks.append(
                f"{source_id}\n{chunk['text'].strip()}\n"
            )

            token_count += tokens
            meta = chunk.get("metadata", {})

            sources.append({
                "source_id": source_id,
                "file": meta.get("source"),
                "page": meta.get("page"),
                "retrieval_type": chunk.get("retrieval_type"),
                "retrieval_score": chunk.get("score"),
                "rerank_score": chunk.get("rerank_score")
            })

        return {
            "context": "\n".join(context_blocks),
            "sources": sources
        }


if __name__ == "__main__":

    query = input("Enter the Query : ")

    retriever = HybridRetriever(top_k=10)
    reranker = Reranker()
    context_builder = ContextBuilder(max_tokens=1200)

    candidates = retriever.hybrid_search(query)

    print("\n HYBRID RESULTS \n")
    for c in candidates:
        print("Type:", c["retrieval_type"])
        print("Score:", c["score"])
        print("Source:", c["metadata"]["source"])
        print("-" * 40)

    reranked = reranker.rerank(
        query,
        candidates,
        top_k=10
    )

    context_payload = context_builder.build_context(
        reranked,
        top_k=5
    )

    print("\n FINAL CONTEXT \n")
    print(context_payload["context"])

    print("\n TRACEABLE SOURCES \n")
    for s in context_payload["sources"]:
        print(s)

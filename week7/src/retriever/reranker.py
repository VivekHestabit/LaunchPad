from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidates, top_k=5):

        if not candidates:
            return []

        pairs = [(query, c["text"]) for c in candidates]

        scores = self.model.predict(pairs)

        reranked_results = []

        for candidate, score in zip(candidates, scores):

            updated = candidate.copy()
            updated["rerank_score"] = float(score)

            reranked_results.append(updated)

        reranked_results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k] ## On the basis of the rerank score we return the top-k searches 

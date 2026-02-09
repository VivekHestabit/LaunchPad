import numpy as np

class MMRSelector:

    def __init__(
        self,
        lambda_param=0.7
    ):
        self.lambda_param = lambda_param

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def select(self, chunks, top_k):

        embeddings = [c["embeddings"] for c in chunks]
        

        selected = []
        selected_idxs = []
        candidate_idxs = list(range(len(chunks)))

        while len(selected) < top_k and candidate_idxs:

            scores = []

            for idx in candidate_idxs:
                relevance = chunks[idx]["rerank_score"]

                if not selected_idxs:
                    diversity_penalty = 0
                else:
                    similarities = [
                        self._cosine_similarity(
                            embeddings[idx],
                            embeddings[s_idx]
                        )
                        for s_idx in selected_idxs
                    ]
                    diversity_penalty = max(similarities)

                mmr_score = (
                    self.lambda_param * relevance
                    - (1 - self.lambda_param) * diversity_penalty
                )

                scores.append((idx, mmr_score))

            best_idx = max(scores, key=lambda x: x[1])[0]

            selected.append(chunks[best_idx])
            selected_idxs.append(best_idx)
            candidate_idxs.remove(best_idx)

        return selected

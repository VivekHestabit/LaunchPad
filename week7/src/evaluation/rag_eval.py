import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity


class RAGEvaluator:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def _cosine(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def faithfulness_score(self, answer, context):
        context_texts = [c["text"] for c in context]
        
        if not context_texts:
            return 0.0

        context_emb = self.model.encode(context_texts)
        answer_emb = self.model.encode(answer)

        similarities = cosine_similarity(
            [answer_emb],
            context_emb
        )[0]

        return float(similarities.max())


    def hallucination_risk(self, score: float) -> str:
        if score >= 0.75:
            return "LOW"
        if score >= 0.5:
            return "MEDIUM"
        return "HIGH"

    def confidence_score(self, score: float) -> float:
        return round(min(max(score, 0.0), 1.0), 2)

    def evaluate(self, answer: str, context: str) -> Dict:
        faithfulness = self.faithfulness_score(answer, context)

        return {
            "faithfulness": faithfulness,
            "confidence": self.confidence_score(faithfulness),
            "hallucination_risk": self.hallucination_risk(faithfulness)
        }

    def refine_answer(
        self,
        question: str,
        draft_answer: str,
        context: str
    ) -> str:
        """
        Self-reflection / refinement loop.
        In real systems this calls an LLM again.
        For capstone, we simulate logic.
        """

        score = self.faithfulness_score(draft_answer, context)

        if score < 0.5:
            return (
                "Based on the available context, there is insufficient "
                "information to answer this question reliably."
            )

        return draft_answer

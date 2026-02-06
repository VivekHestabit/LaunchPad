from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL_NAME
COLLECTION_NAME = "enterprise_rag"

class Retriever:
    def __init__(self, top_k=5):
        self.top_k = top_k
        self.client = QdrantClient(path="src/vectorstore/qdrant")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def search(self, query: str):
        query_vector = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=self.top_k
        )

        return [
            {
                "score": hit.score,
                "payload": hit.payload
            }
            for hit in results
        ]


if __name__ == "__main__":
    retriever = Retriever(top_k=5)
    results = retriever.search(" Tell me about the simon king ")

    for r in results:
        print(r["score"])
        print(r["payload"]["meta_data"])
        print(r["payload"]["text"][:400])
        print("-" * 50)
        print(r["payload"])
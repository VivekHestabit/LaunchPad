from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL_NAME
COLLECTION_NAME = "enterprise_rag"

class Retriever:
    def __init__(self, top_k=5):
        self.top_k = top_k
        self.client = QdrantClient(qdrant_url="http://localhost:6333")
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
    query = input("Enter the Query : ")
    
    results = retriever.search(query)

    for r in results:
        print("Score : " , r["score"])
        print("MetaData : " , r["payload"]["meta_data"])
        print("Text Extracted : " + r["payload"]["text"][:400])
        print("-" * 80)
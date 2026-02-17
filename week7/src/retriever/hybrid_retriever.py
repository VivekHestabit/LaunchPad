import json
from rank_bm25 import BM25Okapi
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL_NAME , EMBEDDINGS_DATA_PATH
import numpy as np
 
COLLECTION_NAME = "enterprise_rag"


class HybridRetriever:

    def __init__(self, top_k=5):

        self.top_k = top_k
        self.client = QdrantClient(url="http://localhost:6333")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.embeddings = np.load(EMBEDDINGS_DATA_PATH)
        
        self.chunks = []
        self.corpus = []

        with open("src/data/chunks/chunks.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)

                self.chunks.append(record)

                self.corpus.append(
                    record["text"].lower().split()
                )

        self.bm25 = BM25Okapi(self.corpus)

    def semantic_search(self, query):

        query_vector = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=self.top_k
        )

        semantic_hits = []

        for hit in results:

            payload = hit.payload
            chunk_index = payload["meta_data"]["chunk_index"]
            
            semantic_hits.append({
                "score": float(hit.score),
                "text": payload["text"],
                "embeddings" : self.embeddings[chunk_index],
                "metadata": payload["meta_data"],
                "retrieval_type": "semantic"
            })

        return semantic_hits

    def keyword_search(self, query):

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:self.top_k]

        keyword_hits = []

        for idx in top_indices:

            chunk = self.chunks[idx]

            keyword_hits.append({
                "score": float(scores[idx]),
                "text": chunk["text"],
                "embeddings" : self.embeddings[idx],
                "metadata": chunk["metadata"],
                "retrieval_type": "keyword"
            })
        return keyword_hits

    def hybrid_search(self, query):

        semantic_results = self.semantic_search(query)
        keyword_results = self.keyword_search(query)

        combined = {}

        for result in semantic_results + keyword_results:

            chunk_index = result["metadata"]["chunk_index"]

            if chunk_index not in combined:
                combined[chunk_index] = result
            else:
                combined[chunk_index]["retrieval_type"] = "hybrid"

        return list(combined.values())
    
    
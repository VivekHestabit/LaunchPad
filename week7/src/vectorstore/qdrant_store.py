import json
import numpy as np
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams , Distance , PointStruct

embedding_path = Path("src/data/embeddings/embeddings.npy")
metadata_path = Path("src/data/embeddings/metadata.jsonl")
chunk_path = Path("src/data/chunks/chunks.jsonl")


COLLECTION_NAME = "enterprise_rag"

vectors = np.load(embedding_path)

metadata = [] 

chunks = [] 


with open(chunk_path, "r", encoding="utf-8") as f:
    for line in f:
        chunks.append(json.loads(line))
        
with open(metadata_path , "r" , encoding="utf-8") as f:
    for line in f:
        metadata.append(json.loads(line))
        
client = QdrantClient(path="src/vectorstore/qdrant")


client.recreate_collection(
    collection_name=COLLECTION_NAME , 
    vectors_config=VectorParams(
        size=vectors.shape[1],
        distance=Distance.COSINE
    )
)

points = [] 

for idx , (vector , meta , chunk) in enumerate(zip(vectors , metadata , chunks)):
    points.append(
            PointStruct(
                id = idx,
                vector=vector.tolist(),
                payload={
                    "meta_data" : meta,
                    "text" : chunk["text"]
                }
            )
    )

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("Qdrant collection created")
print("Vectors stored with metadata")
print(f"Total vectors : {len(points)}")
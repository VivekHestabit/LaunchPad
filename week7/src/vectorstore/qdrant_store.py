import json
import numpy as np
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

EMBEDDING_PATH = Path("src/data/embeddings/embeddings.npy")
METADATA_PATH = Path("src/data/embeddings/metadata.jsonl")
CHUNK_PATH = Path("src/data/chunks/chunks.jsonl")

COLLECTION_NAME = "enterprise_rag"
QDRANT_URL = "http://localhost:6333"

BATCH_SIZE = 256

vectors = np.load(EMBEDDING_PATH)

metadata = []
chunks = []

with open(CHUNK_PATH, "r", encoding="utf-8") as f:
    for line in f:
        chunks.append(json.loads(line))

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        metadata.append(json.loads(line))

client = QdrantClient(
    url=QDRANT_URL,
    timeout=60
)

if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=vectors.shape[1],
        distance=Distance.COSINE
    )
)

total = len(vectors)
print(f"Starting ingestion of {total} vectors...")

for start in range(0, total, BATCH_SIZE):
    end = min(start + BATCH_SIZE, total)
    batch_points = []

    for i in range(start, end):
        content = chunks[i]["text"]
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, content))

        batch_points.append(
            PointStruct(
                id=point_id,
                vector=vectors[i].tolist(),
                payload={
                    "meta_data": metadata[i],
                    "text": content
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=batch_points
    )

    print(f"Ingested {end}/{total}")

print("✅ Ingestion completed successfully")

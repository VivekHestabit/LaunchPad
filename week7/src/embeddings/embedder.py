import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

chunk_file = Path("src/data/chunks/chunks.jsonl")
output_dir = Path("src/data/embeddings")
output_dir.mkdir(parents=True, exist_ok=True)

embeddings_file = output_dir / "embeddings.npy"
metadata_file = output_dir / "metadata.jsonl"

model = SentenceTransformer("BAAI/bge-base-en")

texts = []
metadata = []

with open(chunk_file, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        text = record["text"].strip()

        if not text:
            continue

        texts.append(text)

        metadata.append({
            "source": record["metadata"].get("source"),
            "file_path": record["metadata"].get("file_path"),
            "page": record["metadata"].get("page"),
            "chunk_index": record["metadata"].get("chunk_index")
        })

vectors = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)

np.save(embeddings_file, vectors)

with open(metadata_file, "w", encoding="utf-8") as f:
    for m in metadata:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")

print(" Embeddings generated")
print(" Vectors saved")
print(" Metadata saved")

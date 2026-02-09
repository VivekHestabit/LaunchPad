from qdrant_client import QdrantClient
from src.embeddings.clip_embedder import CLIPEmbedder
import subprocess


class ImageSearcher:

    def __init__(
        self,
        collection_name="image_rag",
        top_k=5,
        qdrant_path="src/vectorstore/qdrant"
    ):
        self.top_k = top_k
        self.collection_name = collection_name
        self.qdrant = QdrantClient(path=qdrant_path)
        self.clip = CLIPEmbedder()

        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        if not self.qdrant.collection_exists(self.collection_name):
            raise RuntimeError(
                f"Collection '{self.collection_name}' does not exist. "
                f"Run image ingestion first."
            )

    def search_by_text(self, query: str):
        query_vector = self.clip.embed_text(query)

        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=self.top_k
        ).points

        return self._format_results(results)

    def search_by_image(self, image_path: str):
        query_vector = self.clip.embed_image(image_path)

        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=self.top_k
        ).points

        return self._format_results(results)

    def image_to_text(self, image_path: str):
        query_vector = self.clip.embed_image(image_path)

        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=self.top_k
        ).points

        texts = []

        for r in results:
            caption = r.payload.get("caption")
            ocr_text = r.payload.get("ocr_text")

            if caption:
                texts.append(f"Caption: {caption}")

            if ocr_text and ocr_text.strip():
                texts.append(f"OCR Text: {ocr_text.strip()}")

        return texts

    def _format_results(self, results):
        formatted = []

        for r in results:
            formatted.append({
                "id": r.id,
                "score": r.score,
                "caption": r.payload.get("caption"),
                "ocr_text": r.payload.get("ocr_text"),
                "source": r.payload.get("source"),
                "page": r.payload.get("page"),
                "type": r.payload.get("type")
            })

        return formatted


if __name__ == "__main__":

    searcher = ImageSearcher(top_k=3)

    mode = input("Search mode (text / image / image_to_text): ").strip().lower()

    if mode == "image":
        query = input("Enter image path: ")
        results = searcher.search_by_image(query)

        for r in results:
            print("Score:", r["score"])
            print("Caption:", r["caption"])
            print("Source:", r["source"])
            subprocess.run(["timg", r["source"]])
            print("-" * 40)

    elif mode == "image_to_text":
        query = input("Enter image path: ")
        texts = searcher.image_to_text(query)

        for t in texts:
            print(t)
            print("-" * 40)

    else:
        query = input("Enter text query: ")
        results = searcher.search_by_text(query)

        for r in results:
            print("Score:", r["score"])
            print("Caption:", r["caption"])
            print("Source:", r["source"])
            subprocess.run(["timg", r["source"]])
            print("-" * 40)

import uuid
import os
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from src.embeddings.clip_embedder import CLIPEmbedder


class ImageIngestor:

    def __init__(
        self,
        collection_name="image_rag",
        qdrant_url="http://localhost:6333"
    ):
        self.collection_name = collection_name
        self.qdrant = QdrantClient(url=qdrant_url)
        self.clip = CLIPEmbedder()

        self._ensure_collection()

        self.caption_processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.caption_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def _ensure_collection(self):
        if not self.qdrant.collection_exists(self.collection_name):
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=512,
                    distance=Distance.COSINE
                )
            )
    def extract_ocr(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(image).strip()

    def generate_caption(self, image: Image.Image) -> str:
        inputs = self.caption_processor(
            images=image,
            return_tensors="pt"
        )

        output = self.caption_model.generate(**inputs)

        caption = self.caption_processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption

    def ingest_image(
        self,
        image_path: str,
        source: str = None,
        page: int = None
    ):
        image = Image.open(image_path).convert("RGB")

        ocr_text = self.extract_ocr(image)
        caption = self.generate_caption(image)
        image_vector = self.clip.embed_image(image_path).tolist()

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=image_vector,
            payload={
                "type": "image",
                "source": source or image_path,
                "page": page,
                "caption": caption,
                "ocr_text": ocr_text
            }
        )
        
        print("INGEST VECTOR TYPE:", type(image_vector))
        print("INGEST VECTOR DIM:", len(image_vector))
        print("INGEST VECTOR SAMPLE:", image_vector[:5])


        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        return {
            "image_path": image_path,
            "caption": caption,
            "ocr_text": ocr_text
        }


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_ROOT = os.path.join(BASE_DIR, "..", "data", "raw", "Images")

    ingestor = ImageIngestor()

    count = 0

    for root, _, files in os.walk(IMAGE_ROOT):
        for file_name in files:
            if not file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            image_path = os.path.join(root, file_name)

            ingestor.ingest_image(
                image_path=image_path,
                source=image_path,
                page=None
            )

            print("Ingested:", image_path)
            count += 1

    if count == 0:
        print("❌ NO IMAGES FOUND — NOTHING INGESTED")
    else:
        print(f"✅ {count} IMAGES INGESTED SUCCESSFULLY")


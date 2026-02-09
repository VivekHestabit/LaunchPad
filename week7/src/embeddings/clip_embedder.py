from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel


class CLIPEmbedder:

    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_image(self, image_path: str):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)

        image_features = outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy()[0]

    def embed_text(self, text: str):
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs)

        text_features = outputs.pooler_output
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy()[0]


if __name__ == "__main__":

    embedder = CLIPEmbedder()

    text_vector = embedder.embed_text(
        "credit underwriting flow diagram"
    )

    print("Text embedding dimension:", len(text_vector))

# Multimodal Retrieval-Augmented Generation (RAG) System

This document describes the design, architecture, and workflow of the Multimodal Retrieval system implemented in this project.

The system focuses on image-centric multimodal retrieval, enabling text and image understanding using CLIP embeddings, OCR grounding, and a Qdrant vector database.

This implementation represents the retrieval foundation of a Multimodal RAG pipeline.

---

## 1. Problem Statement

Traditional RAG systems operate only on text.  
However, real-world data often contains important information in visual form, such as:

- Scanned documents
- Engineering diagrams
- Forms and invoices
- Screenshots
- Images with embedded text

Pure text-based RAG systems fail to capture this information.

This system extends retrieval to multimodal inputs by supporting:

- Text → Image retrieval
- Image → Image retrieval
- Image → Text retrieval
- OCR grounding to reduce hallucinations

---

## 2. High-Level Architecture

User Query (Text or Image)
│
▼
CLIP Encoder
(Text / Image)
│
▼
Vector Database (Qdrant)
│
▼
Top-K Relevant Images
│
▼
Context Builder
(OCR + Captions + Metadata)
│
▼
Retrieved Context


This implementation focuses on retrieval and grounding.  
LLM-based generation can be added in later stages.

---

## 3. Supported Modalities

### 3.1 Ingested Data Types

- JPEG images
- PNG images
- JPG images

---

### 3.2 Generated Representations

For each ingested image, the system generates:

- OCR text (exact text from the image)
- Caption (semantic description of the image)
- CLIP image embedding (visual semantics)
- CLIP text embedding (cross-modal alignment)
- Metadata (source path, page, type)

These representations are stored together to ensure traceability and grounding.

---

## 4. Image Ingestion Pipeline

### File

`pipelines/image_ingest.py`

### Responsibilities

- Recursively scan `src/data/raw/Images/`
- For each image:
  - Load and preprocess the image
  - Extract OCR text using Tesseract
  - Generate a semantic caption
  - Generate a CLIP image embedding
  - Store embedding and metadata in Qdrant

---

### Example Stored Payload

```json
{
  "type": "image",
  "source": "src/data/raw/Images/sample.png",
  "page": null,
  "caption": "a block diagram of a power supply",
  "ocr_text": "INPUT VOLTAGE 230V AC"
}
```

# Embedding Pipeline (CLIP)

## File

`embeddings/clip_embedder.py`

## Why CLIP?

CLIP embeds text and images into the same vector space, enabling:

- Text → Image retrieval
- Image → Image retrieval
- Image → Text retrieval

## Embedding Characteristics

- Vector dimension: 512
- Same embedding space for text and images
- Cosine similarity for comparison

---

# Vector Storage (Qdrant)

The system uses local (embedded) Qdrant for vector storage.

## Key Details

- Vector database: Qdrant
- Storage mode: Local filesystem (`path=`)
- Collection name: Images
- Vector type: Dense (CLIP embeddings)

## Why Qdrant?

- Fast vector similarity search
- Metadata and vector storage together
- Easy inspection and debugging
- No Docker required for local mode

---

# Retrieval Layer

## File

`retriever/image_search.py`

The retrieval layer supports three query modes.

---

## Text → Image Retrieval

### Input

- Text query

### Process

- Encode text using CLIP
- Search against image embeddings in Qdrant

### Output

- Relevant images
- Captions and OCR text

---

## Image → Image Retrieval

### Input

- Image query

### Process

- Encode image using CLIP
- Search for visually and semantically similar images

### Output

- Similar images with metadata

---

## Image → Text Retrieval

### Input

- Image query

### Process

- Retrieve similar images
- Extract captions and OCR text

### Output

- Textual context derived from images

This mode acts as the bridge from vision to language.

---

# OCR vs Caption (Critical Distinction)

OCR and captions serve different purposes and are both required.

## OCR

- Extracts exact text from images
- Provides factual grounding
- Prevents hallucinations

## Caption

- Provides semantic understanding
- Describes visual meaning
- Improves retrieval recall

Using both ensures high-precision multimodal retrieval.

---

# Hallucination Control
```
Hallucinations are reduced by:

- OCR-based grounding
- Caption-based semantic validation
- Metadata traceability
- Source-aware retrieval

Every retrieved result can be traced back through:
```

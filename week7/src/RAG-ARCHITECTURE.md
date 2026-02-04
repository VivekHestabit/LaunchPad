# RAG Architecture (Retrieval-Augmented Generation)

## Overview

Retrieval-Augmented Generation (RAG) is an architecture that combines **information retrieval** with **text generation** to produce accurate, context-aware responses.

Instead of relying only on a Large Language Model’s internal knowledge, RAG **retrieves relevant information from an external knowledge base** and uses it to ground the generated answer.

---

## High-Level RAG Architecture

User Query
│
▼
Retriever
│
▼
Vector Database
│
▼
Top-K Relevant Chunks
│
▼
Generator (LLM)
│
▼
Final Answer


RAG is composed of **two main subsystems**:
1. **Retriever**
2. **Generator**

---

## Core Components

### 1. Knowledge Base

The knowledge base contains the source documents used by the system.

Examples:
- PDFs
- Markdown files
- Text files
- CSVs
- Internal enterprise documents

These documents are treated as the **source of truth** and are not modified.

---

### 2. Chunking Layer

Large documents are split into smaller, semantically meaningful chunks.

Typical strategy:
- Chunk size: 500–800 tokens
- Chunk overlap: 50–150 tokens

**Why chunking is required:**
- LLMs have token limits
- Embeddings work better on smaller text
- Improves retrieval precision

Each chunk is usually stored with metadata such as:
- Source document
- Page number
- Section or chunk index

---

### 3. Embedding Model

Each chunk is converted into a **dense numerical vector** using an embedding model.

Characteristics:
- High-dimensional vectors (e.g., 384, 768)
- Capture semantic meaning
- Similar text → closer vectors

The same embedding model is used for:
- Document chunks
- User queries

---

### 4. Vector Database (Retriever Backend)

A vector database stores:
- Embeddings
- Optional metadata or payload

Its responsibility is to:
- Perform similarity search
- Return the most relevant chunks for a query

Common similarity metrics:
- Cosine similarity
- Dot product
- Euclidean distance

The vector database enables **semantic search**, not keyword matching.

---

### 5. Retriever

The retriever performs the following steps:
1. Convert user query into an embedding
2. Search the vector database
3. Retrieve top-K most similar chunks

Output:
- Relevant chunks
- Similarity scores
- Associated metadata

The retriever **does not generate text** — it only finds relevant information.

---

### 6. Generator (LLM)

The generator is a Large Language Model that:
- Takes the user query
- Takes retrieved chunks as context
- Generates a grounded answer

The retrieved content is injected into the prompt, ensuring:
- Factual grounding
- Reduced hallucinations
- Domain-specific accuracy

---

## End-to-End RAG Flow

1. User submits a query
2. Query is embedded
3. Vector database retrieves relevant chunks
4. Retrieved chunks are added to the prompt
5. LLM generates the final response
6. Answer is returned to the user

---

## Why RAG Is Important

- Keeps LLM responses grounded in real data
- Avoids retraining models for new knowledge
- Supports private and enterprise data
- Reduces hallucinations
- Enables explainability and citations

---

## Key Design Decisions in RAG

- Chunk size vs overlap
- Choice of embedding model
- Vector database selection
- Whether to store text inside the vector DB or externally
- Prompt construction strategy

---

## Summary

RAG separates **knowledge retrieval** from **language generation**.

- Retriever → finds relevant information
- Generator → synthesizes an answer

This separation makes RAG:
- Scalable
- Modular
- Enterprise-ready

RAG is the foundation of modern AI systems used for:
- Chatbots
- Document QA
- Enterprise search
- Knowledge assistants
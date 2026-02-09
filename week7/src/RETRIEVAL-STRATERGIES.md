# Day 2 — Advanced Retrieval and Context Engineering

This document describes the **advanced retrieval system** implemented on Day 2, focusing on **hybrid retrieval strategies**, **reranking**, **MMR**, and **context construction** for improving LLM answer quality.

The system is designed to **maximize precision**, **minimize hallucinations**, and provide **fully traceable context** using a Qdrant-based vector database.

---

## Overview

Day 2 builds on basic semantic retrieval by introducing:

- Hybrid retrieval (semantic + keyword)
- Reranking for improved relevance
- Max Marginal Relevance (MMR)
- Context deduplication
- Structured context building for LLMs

This day focuses purely on **retrieval intelligence and context engineering**, not generation.

---

## Retrieval Strategies

This system uses a **hybrid retrieval approach** to balance recall and precision.

---

## 1. Vector Retrieval (Semantic Search)

- Dense vector similarity search using embeddings
- Cosine similarity metric
- Implemented using **Qdrant**
- Acts as the **primary recall mechanism**

Semantic retrieval captures conceptual similarity and meaning.

---

## 2. Keyword Retrieval (BM25)

Keyword search is used as a **fallback and complement** to semantic retrieval.

It helps handle:

- Rare or out-of-vocabulary terms
- IDs and reference numbers
- Financial and legal jargon
- Exact keyword matching

BM25 ensures **recall safety** when embeddings alone are insufficient.

---

## 3. Hybrid Retrieval

Semantic and keyword results are **merged together** to form a candidate pool.

Benefits:
- Combines semantic understanding with lexical precision
- Improves robustness across query types
- Reduces false negatives

---

## 4. Metadata-Based Filtering

Metadata filters are applied during retrieval to scope results.

Examples:
- `document_type`
- `source`
- `domain`
- `year`

Filtering ensures that only **relevant and valid documents** are retrieved.

---

## 5. Deduplication

Deduplication is applied after retrieval to:

- Remove repeated or overlapping chunks
- Prevent redundant context
- Reduce token wastage in LLM prompts

This improves signal-to-noise ratio.

---

## 6. Reranking

Retrieved candidates are reranked using relevance scoring.

### Reranking Strategy

- Cross-encoder based reranking
- Query–chunk relevance scoring
- Reorders results based on semantic accuracy

Reranking significantly improves **precision at top-K**.

---

## 7. Max Marginal Relevance (MMR)

MMR is applied to balance:

- Relevance
- Diversity

Benefits:
- Prevents similar chunks from dominating the context
- Ensures broader coverage of information
- Improves answer completeness

---

## 8. Context Builder

The context builder prepares the final input for the LLM.

### Responsibilities

- Select top-ranked chunks
- Apply deduplication and MMR
- Respect LLM context window limits
- Preserve source metadata for traceability

The output is a **clean, ranked, LLM-ready context**.

---

## 9. Traceable Context

Every retrieved chunk includes:

- Source document
- Chunk ID
- Metadata fields
- Retrieval score

This enables:
- Explainability
- Auditing
- Debugging
- Trustworthy LLM outputs

---

## Result

The Day 2 retrieval system achieves:

- ✔ Higher precision
- ✔ Lower hallucination
- ✔ Fully traceable context

---

## Summary

Day 2 introduces **production-grade retrieval techniques** by combining:

- Semantic search
- Keyword search (BM25)
- Reranking
- MMR
- Context engineering

This forms a **strong retrieval foundation** for reliable and explainable RAG systems.

---

## Next Step

- Integrate this retrieval system with an LLM
- Extend retrieval to multimodal data (Day 3)
- Add evaluation metrics for retrieval quality

# DAY 5 — ADVANCED RAG + MEMORY + EVALUATION (CAPSTONE)

## Overview

This capstone project integrates all components from Week 7 into a production-ready multimodal RAG system with memory, evaluation, and self-reflection capabilities. The system provides three core modes of operation: Text RAG, Image RAG, and SQL Question Answering.

## 🎯 Learning Outcomes

- ✅ Conversational memory with context retention
- ✅ Self-reflection and answer refinement loops
- ✅ Hallucination detection and risk assessment
- ✅ Faithfulness scoring for answer quality
- ✅ Production-ready API structure with FastAPI
- ✅ Interactive Streamlit UI for user interaction

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI (ui.py)                  │
│          Text RAG | Image RAG | SQL Assistant            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (app.py)                    │
│  Endpoints: /ask | /ask-image | /ask-image-image |       │
│             /ask-sql                                     │
└──────┬────────────┬─────────────┬─────────────┬─────────┘
       │            │             │             │
       ▼            ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Hybrid   │ │  Image   │ │   SQL    │ │   Memory     │
│Retriever │ │ Searcher │ │ Pipeline │ │    Store     │
└──────────┘ └──────────┘ └──────────┘ └──────────────┘
       │            │             │             │
       └────────────┴─────────────┴─────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  RAG Evaluator  │
              │  - Faithfulness │
              │  - Confidence   │
              │  - Hallucination│
              └─────────────────┘
```

## 📁 File Structure

```
src/
├── deployment/
│   └── app.py              # FastAPI backend with all endpoints
├── evaluation/
│   └── rag_eval.py         # RAG evaluation and refinement logic
├── memory/
│   └── memory_store.py     # Conversation memory management
├── retriever/
│   ├── hybrid_retriever.py # Hybrid text retrieval
│   └── image_search.py     # Image-based retrieval
├── pipelines/
│   └── sql_pipeline.py     # SQL query generation and execution
└── ui.py                   # Streamlit user interface
CHAT-LOGS.json              # Persistent conversation history
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install required packages
pip install fastapi uvicorn streamlit requests pillow
pip install sentence-transformers scikit-learn numpy
```

### Running the System

1. **Start the FastAPI Backend**

```bash
# From project root
uvicorn src.deployment.app:app --reload --port 8000
```

2. **Launch the Streamlit UI**

```bash
# In a separate terminal
streamlit run src/ui.py
```

3. **Access the Application**

- API: `http://localhost:8000`
- UI: `http://localhost:8501`

## 🔧 Core Components

### 1. Memory Store (`memory_store.py`)

**Purpose**: Maintains conversation history and context for multi-turn interactions.

**Key Features**:
- Stores last 5 messages (configurable via `max_messages`)
- Persists to `CHAT-LOGS.json` for durability
- Provides formatted context for prompt injection
- Timestamped entries for audit trails

**Usage**:
```python
from src.memory.memory_store import MemoryStore

memory = MemoryStore(max_messages=5)
memory.add_message("What is RAG?", "RAG stands for...")
context = memory.get_prompt_context()
```

**Storage Format**:
```json
[
  {
    "question": "User query here",
    "answer": "System response here",
    "timestamp": "2026-02-16T10:30:00.123456"
  }
]
```

### 2. RAG Evaluator (`rag_eval.py`)

**Purpose**: Evaluates answer quality and detects hallucination risks.

**Evaluation Metrics**:

| Metric | Description | Range |
|--------|-------------|-------|
| **Faithfulness** | Semantic similarity between answer and context | 0.0 - 1.0 |
| **Confidence** | Normalized faithfulness score | 0.0 - 1.0 |
| **Hallucination Risk** | Categorical risk assessment | LOW/MEDIUM/HIGH |

**Risk Thresholds**:
- **LOW**: Faithfulness ≥ 0.75 (Strong alignment with context)
- **MEDIUM**: 0.5 ≤ Faithfulness < 0.75 (Moderate alignment)
- **HIGH**: Faithfulness < 0.5 (Weak alignment, possible hallucination)

**Key Methods**:

```python
evaluator = RAGEvaluator()

# Evaluate answer quality
scores = evaluator.evaluate(answer, context)
# Returns: {'faithfulness': 0.82, 'confidence': 0.82, 'hallucination_risk': 'LOW'}

# Refine answer with self-reflection
refined = evaluator.refine_answer(question, draft_answer, context)
# Returns improved answer or safety message
```

**Self-Reflection Logic**:
- If faithfulness < 0.5: Returns safety message about insufficient context
- Otherwise: Returns the draft answer as-is
- In production: Would trigger an LLM re-generation loop

### 3. FastAPI Backend (`app.py`)

**Endpoints**:

#### `/ask` (POST) - Text RAG

**Parameters**:
- `question` (str): User's text query

**Workflow**:
1. Retrieve relevant chunks using hybrid retrieval
2. Generate initial answer from top chunk
3. Refine answer using self-reflection
4. Evaluate faithfulness and risk
5. Store in memory
6. Return traced response

**Response**:
```json
{
  "trace_id": "uuid-here",
  "answer": "Refined answer text",
  "context_used": [
    {
      "text": "Context chunk",
      "score": 0.85,
      "retrieval_type": "hybrid",
      "metadata": {}
    }
  ],
  "evaluation": {
    "faithfulness": 0.82,
    "confidence": 0.82,
    "hallucination_risk": "LOW"
  },
  "timestamp": 1708084800.123
}
```

#### `/ask-image` (POST) - Image RAG (Text → Image or Image → Text)

**Parameters**:
- `question` (Form, optional): Text query for image search
- `image` (File, optional): Uploaded image for OCR extraction

**Modes**:

**Mode 1: Text → Image**
- Input: Text query
- Output: List of relevant images with metadata

**Mode 2: Image → Text**
- Input: Uploaded image
- Process: OCR extraction + text recognition
- Output: Extracted text with evaluation scores

**Response (Image → Text)**:
```json
{
  "trace_id": "uuid-here",
  "answer": "Extracted text from image",
  "context_used": [],
  "evaluation": {
    "faithfulness": 0.75,
    "confidence": 0.75,
    "hallucination_risk": "LOW"
  },
  "timestamp": 1708084800.123
}
```

#### `/ask-image-image` (POST) - Image Similarity Search

**Parameters**:
- `image` (File, required): Query image

**Workflow**:
1. Save uploaded image to temp directory
2. Generate CLIP embeddings
3. Search for similar images in vector store
4. Return ranked results

**Response**:
```json
{
  "trace_id": "uuid-here",
  "answer": "Similar images found",
  "context_used": [
    {
      "source": "/path/to/image.png",
      "caption": "Image description",
      "score": 0.91
    }
  ],
  "timestamp": 1708084800.123
}
```

#### `/ask-sql` (POST) - SQL Question Answering

**Parameters**:
- `question` (str): Natural language database query

**Workflow**:
1. Generate SQL from natural language
2. Validate SQL syntax
3. Execute on database (SQLite/PostgreSQL)
4. Summarize results
5. Store in memory

**Response**:
```json
{
  "trace_id": "uuid-here",
  "answer": "SQL execution result",
  "timestamp": 1708084800.123
}
```

### 4. Streamlit UI (`ui.py`)

**Features**:
- **Mode Selection**: Radio buttons for Text RAG / Image RAG / SQL RAG
- **Dynamic Input**: Text areas for questions, file uploaders for images
- **Image Rendering**: Displays images from URLs or local paths
- **Evaluation Display**: Shows faithfulness, confidence, and hallucination risk
- **Error Handling**: User-friendly error messages

**Image RAG Modes**:
1. **Image → Image**: Find similar images
2. **Image → Text**: Extract text from uploaded image
3. **Text → Image**: Find images matching text description

**Usage Flow**:
```
1. Select mode (Text/Image/SQL)
2. Enter query or upload file
3. Click action button
4. View results with evaluation metrics
```

## 🔍 Memory and Context Management

### Memory Retention

The system maintains **rolling window memory** of the last 5 interactions:

```python
memory_store.add_message(
    question="What is hybrid retrieval?",
    answer="Hybrid retrieval combines..."
)

# Retrieves formatted context for LLM prompts
context = memory_store.get_prompt_context()
```

**Output Format**:
```
User: What is hybrid retrieval?
Assistant: Hybrid retrieval combines semantic and keyword search...
User: How does it reduce hallucination?
Assistant: It reduces hallucination by providing multiple...
```

### Persistent Logging

All conversations are logged to `CHAT-LOGS.json`:

```json
[
  {
    "question": "Explain RAG architecture",
    "answer": "RAG consists of a retriever and generator...",
    "timestamp": "2026-02-16T14:23:10.456789"
  }
]
```

**Benefits**:
- Audit trail for compliance
- Debugging failed queries
- Training data for model fine-tuning
- User behavior analysis

## 📊 Evaluation Framework

### Faithfulness Scoring

**Algorithm**:
1. Generate embeddings for answer and all context chunks
2. Compute cosine similarity between answer and each chunk
3. Return maximum similarity as faithfulness score

**Implementation**:
```python
def faithfulness_score(self, answer, context):
    context_texts = [c["text"] for c in context]
    context_emb = self.model.encode(context_texts)
    answer_emb = self.model.encode(answer)
    
    similarities = cosine_similarity([answer_emb], context_emb)[0]
    return float(similarities.max())
```

### Hallucination Detection

**Risk Categories**:

| Score Range | Risk Level | Interpretation |
|-------------|------------|----------------|
| ≥ 0.75 | LOW | Strong semantic alignment with source |
| 0.5 - 0.74 | MEDIUM | Moderate alignment, needs verification |
| < 0.5 | HIGH | Weak alignment, likely hallucination |

### Self-Reflection Loop

**Refinement Logic**:
```python
def refine_answer(self, question, draft_answer, context):
    score = self.faithfulness_score(draft_answer, context)
    
    if score < 0.5:
        return "Insufficient information to answer reliably."
    
    return draft_answer  # In production: trigger LLM re-generation
```

**Future Enhancements**:
- Multi-round refinement with LLM critique
- Chain-of-thought reasoning for complex queries
- Retrieval augmentation for low-confidence answers

## 🛡️ Error Handling and Safety

### Input Validation

```python
if not question and not image:
    return {"error": "Provide text or image"}
```

### Image Processing Safety

```python
try:
    if source.startswith("http"):
        resp = requests.get(source, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
    else:
        if not os.path.exists(source):
            st.warning(f"Image not found: {source}")
            return
        img = Image.open(source)
except Exception as e:
    st.warning(f"Could not render image: {e}")
```

### Timeout Protection

All API calls include timeout guards:
```python
resp = requests.post(endpoint, data=data, timeout=600)
```

## 📈 Performance Optimization

### Context Serialization

Efficient serialization prevents float serialization errors:

```python
def serialize_context(context):
    cleaned = []
    for c in context:
        cleaned.append({
            "text": c.get("text"),
            "score": float(c.get("score", 0.0)),  # Convert to native float
            "retrieval_type": c.get("retrieval_type"),
            "metadata": c.get("metadata", {})
        })
    return cleaned
```

### Image Context Normalization

Combines OCR and captions for multimodal retrieval:

```python
def normalize_image_context(context):
    normalized = []
    for c in context:
        if c.get("caption"):
            normalized.append({"text": c["caption"]})
        if c.get("ocr_text"):
            normalized.append({"text": c["ocr_text"]})
    return normalized
```

## 🧪 Testing the System

### Test Case 1: Text RAG

**Input**:
```
Question: "Explain hybrid retrieval strategies"
```

**Expected Output**:
- Answer retrieved from top semantic chunk
- Faithfulness score ≥ 0.7
- Hallucination risk: LOW
- Context sources traceable

### Test Case 2: Image → Text

**Input**:
```
Upload: scanned_invoice.png
```

**Expected Output**:
- Extracted text via OCR
- Evaluation scores
- Memory entry: "image_to_text"

### Test Case 3: SQL Query

**Input**:
```
Question: "Show total sales by product category"
```

**Expected Output**:
- Generated SQL query
- Executed results
- Formatted summary

### Test Case 4: Memory Persistence

**Steps**:
1. Ask 5 questions
2. Restart application
3. Check `CHAT-LOGS.json`

**Expected**:
- Last 5 interactions preserved
- Timestamps accurate
- No data loss

## 🚧 Known Limitations and Future Work

### Current Limitations

1. **Simplified Refinement**: Self-reflection doesn't call LLM for re-generation
2. **Basic OCR**: Tesseract may struggle with handwritten text
3. **Single Language**: No multilingual support
4. **No Streaming**: Responses are not streamed to UI

### Planned Enhancements

- [ ] Multi-round refinement with GPT-4/Claude
- [ ] Streaming responses via WebSockets
- [ ] Redis for distributed memory
- [ ] Prometheus metrics integration
- [ ] A/B testing framework for retrieval strategies
- [ ] Human feedback loop (thumbs up/down)
- [ ] Citation links to source documents
- [ ] Multi-language support

## 📚 Dependencies

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
streamlit==1.31.0
requests==2.31.0
pillow==10.2.0
sentence-transformers==2.3.1
scikit-learn==1.4.0
numpy==1.26.3
python-multipart==0.0.6
```

## 🎓 Learning Checklist

- [x] Implemented conversational memory with rolling window
- [x] Built RAG evaluation framework with faithfulness scoring
- [x] Integrated hallucination detection
- [x] Created self-reflection/refinement loop
- [x] Deployed production-ready FastAPI endpoints
- [x] Built interactive Streamlit UI
- [x] Handled multimodal inputs (text + images)
- [x] Implemented SQL question answering
- [x] Added comprehensive error handling
- [x] Logged all interactions for debugging

## 🏆 Completion Criteria

| Feature | Status |
|---------|--------|
| Text RAG | ✅ Implemented |
| Image RAG | ✅ Implemented |
| SQL QA | ✅ Implemented |
| Memory Store | ✅ Implemented |
| Evaluation Metrics | ✅ Implemented |
| Refinement Loop | ✅ Implemented |
| API Endpoints | ✅ Implemented |
| UI Interface | ✅ Implemented |
| Logging | ✅ Implemented |
| Documentation | ✅ Complete |

## 📝 Next Steps

1. **Deploy to Production**: Containerize with Docker
2. **Add Monitoring**: Integrate Grafana + Prometheus
3. **Scale Retrieval**: Move to Qdrant/Weaviate for production
4. **Security Hardening**: Add authentication, rate limiting
5. **Multi-Agent Extension**: Build orchestration layer for Week 8

## 🤝 Contributing

To extend this capstone:

1. Add new retrieval strategies in `/retriever/`
2. Enhance evaluation metrics in `rag_eval.py`
3. Build new endpoints in `app.py`
4. Update UI in `ui.py`
5. Document changes in this README

## 📄 License

This project is part of Week 7 GenAI internship curriculum.

---


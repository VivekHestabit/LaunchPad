# Day 4 — Agentic AI Week: Memory Architecture

## Overview

Day 4 focuses on building a **persistent memory system** for an AI agent. The system is composed of three layers of memory that work together to give the agent both short-term awareness and long-term recall.

---

## Memory Layers

### 1. Session Memory (`SessionMemory`)
- Stores the **current conversation** in a rolling buffer.
- Keeps track of recent messages (User + Agent turns).
- Used to provide immediate conversational context to the agent.

### 2. Vector Memory (`VectorStore`)
- Uses **FAISS index** to store dense vector embeddings of facts.
- Enables **semantic similarity search** over stored memories.
- Returns `(memory_id, similarity_score)` pairs ranked by relevance.

### 3. Long-Term Memory (`LongTermMemory`)
- Backed by a **SQLite database**.
- Stores structured facts with metadata: `category`, `importance`.
- Looked up by `memory_id` after vector search narrows candidates.

---

## Core Components

### `MemoryManager`

The central orchestrator that coordinates all three memory layers.

```python
class MemoryManager:
    def __init__(self):
        self.session = SessionMemory()
        self.vector = VectorStore()
        self.long_term = LongTermMemory()
        self.llm = OpenAI(...)  # Groq-hosted model
```

---

## Key Methods

### `store_interaction(user_msg, agent_msg)`

Called after every conversation turn.

1. Appends both messages to **Session Memory**.
2. Runs the **Summarizer LLM** to extract facts from the exchange.
3. Filters out low-importance facts (`importance < 0.5`).
4. Calls `reconcile_and_store()` for each surviving fact.

```
User + Agent Message
        │
        ▼
   Summarizer LLM
        │
        ▼
  [fact, category, importance]
        │
   importance >= 0.5?
        │
        ▼
 reconcile_and_store()
```

---

### `summarize(text)`

Prompts the LLM to extract **long-term semantic facts** about the user.

- Returns a JSON list of `{ fact, category, importance }` objects.
- Only stores facts about: preferences, identity, goals, projects, skills, constraints.
- Ignores: greetings, small talk, assistant explanations.

---

### `retrieve_context(query)`

Builds the full memory context injected into the agent's prompt.

1. Fetches **recent session messages**.
2. Performs **vector search** (`k=3`) to find semantically similar facts.
3. Fetches full fact text from **SQLite** using returned `memory_id`s.
4. Returns a formatted string with both session and long-term context.

```
Query
  │
  ├── Session Memory  →  recent conversation turns
  └── Vector Search   →  top-3 memory_ids
            │
            ▼
       SQLite Lookup
            │
            ▼
   "SESSION MEMORY: ...\nRELEVANT FACTS: ..."
```

---

### `reconcile_and_store(fact_obj)`

Prevents duplicate or contradictory facts from polluting memory.

| Score Range | Action |
|---|---|
| `score < SIM_THRESHOLD (0.80)` | Ignore — unrelated fact |
| `score > DUP_THRESHOLD (0.93)` | Skip — near-duplicate |
| `0.80 ≤ score ≤ 0.93` | Send to LLM for reconciliation |

**LLM Reconciliation Labels:**

| Relation | Action |
|---|---|
| `DUPLICATE` | Discard new fact |
| `CONTRADICTS` | Replace old with new |
| `UPDATES` | Replace old with new |
| `MERGEABLE` | Merge into a combined fact |
| `UNRELATED` | Store both independently |

---

### `_store_new_fact(fact_obj)`

Final write step. Only executes if `importance >= 0.5`.

1. Generates a unique `memory_id` (64-bit integer from UUID).
2. Adds the fact text to the **FAISS vector index**.
3. Persists the structured fact to **SQLite**.

---

## Agent Flow (`main.py`)

```
User Input
    │
    ▼
retrieve_context(query)         ← Session + Vector + SQLite
    │
    ▼
Inject into agent prompt
    │
    ▼
AssistantAgent.run()            ← AutoGen + Groq LLM
    │
    ▼
Print answer
    │
    ▼
store_interaction(user, agent)  ← Summarize + Reconcile + Store
```

---

## Thresholds

| Constant | Value | Purpose |
|---|---|---|
| `SIM_THRESHOLD` | `0.80` | Minimum similarity to trigger reconciliation |
| `DUP_THRESHOLD` | `0.93` | Similarity above which fact is treated as duplicate |

---

## Utilities

### `clean_llm_json(text)`
Strips markdown code fences (` ```json `) from LLM output before parsing.

### `safe_json_list(text)` / `safe_json_obj(text)`
Safely extracts a JSON array or object from raw LLM text using regex, with fallback to `[]` / `{}` on failure.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq API (OpenAI-compatible) |
| Agent Framework | AutoGen (`autogen-agentchat`) |
| Vector Search | FAISS |
| Long-Term Store | SQLite |
| Session Store | In-memory rolling buffer |
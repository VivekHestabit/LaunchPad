# Day 4 — SQL Question Answering System (Text → SQL → Answer)

## Overview
This project implements a **schema-aware SQL Question Answering (SQL-QA) system** that allows users to ask **natural language questions** about a database and receive **accurate, validated answers**.

The system uses an **LLM (LLaMA-3.1-8B-Instant via Groq)** to:
- Convert text questions into SQL
- Auto-correct invalid SQL
- Summarize query results in natural language

The database backend is **SQLite**, and the pipeline is designed to be **safe, deterministic, and production-oriented**.

---

## Learning Outcomes
By completing this task, the following concepts were implemented and understood:

- Converting natural language queries into SQL
- Schema-aware reasoning (preventing column hallucination)
- SQL validation and safety checks
- SQLite dialect enforcement
- Automatic SQL error correction using LLM
- Natural language summarization of SQL result tables

---

## Architecture

User Question
↓
Schema Extraction
↓
LLM (Text → SQL)
↓
SQL Validator + Dialect Guard
↓
SQLite Execution
↓
(If error → LLM Auto-Fix → Retry)
↓
LLM Result Summarization


---

## Project Structure
```
week7/
├── load_csv_to_sqlite.py
├── sales.csv
├── src/
│ ├── sales.db
│ ├── pipelines/
│ │ └── sql_pipeline.py
│ ├── generator/
│ │ ├── llm_client.py
│ │ ├── sql_generator.py
│ │ └── test.py
│ └── utils/
│ ├── schema_loader.py
│ └── sql_validator.py
└── README.md
```


---

## Components Description

### 1. CSV Loader (`load_csv_to_sqlite.py`)
- Creates `sales.db`
- Creates `customers` table
- Loads data from `sales.csv`
- Run **once** or when CSV changes

---

### 2. Schema Loader (`schema_loader.py`)
- Extracts table and column names from SQLite
- Converts schema into text for LLM grounding
- Prevents hallucinated columns

---

### 3. SQL Generator (`sql_generator.py`)
- Uses LLM to generate SQL from natural language
- Enforces:
  - SQLite compatibility
  - SELECT-only queries
  - Strict schema usage

---

### 4. SQL Validator (`sql_validator.py`)
- Blocks unsafe SQL:
  - INSERT, UPDATE, DELETE, DROP, ALTER
- Ensures read-only execution

---

### 5. SQL Pipeline (`sql_pipeline.py`)
- Orchestrates the full flow:
  - Text → SQL
  - Validation
  - Execution
  - Auto-fix on failure
  - Result summarization

---

### 6. LLM Client (`llm_client.py`)
- Uses **Groq SDK**
- Model: `llama-3.1-8b-instant`
- Handles:
  - SQL generation
  - SQL auto-correction
  - Result summarization

---

## Database Details

**Database:** SQLite  
**File:** `src/sales.db`  
**Table:** `customers`

**Columns:**
- first_name
- last_name
- company
- city
- country
- phone_1
- phone_2
- email
- subscription_date
- website

---

## How to Run

### Step 1: Activate Virtual Environment
```bash
source venv/bin/activate
Step 2: Load CSV into SQLite
python load_csv_to_sqlite.py
Expected output:

Inserted <N> rows into customers table
Step 3: Run SQL-QA Pipeline
python -m src.pipelines.sql_pipeline
```
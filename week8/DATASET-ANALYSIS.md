# Day 1 — LLM Architecture + Data Prep for Fine-Tuning

## Overview

This repository contains the work completed for **Day 1** of the LLM Fine-Tuning challenge. The focus of this day was on understanding the core architecture of Large Language Models and building a clean, curated **instruction-tuning dataset** for the **Healthcare / Medical** domain from scratch.

---

## Learning Outcomes

- LLM anatomy — layers, attention mechanisms, and Feed-Forward Networks (FFN)
- Tokenization strategies and vocabulary design
- Difference between instruction tuning and pretraining
- LoRA & PEFT fundamentals

---

## Topics Covered

- Transformer blocks and how they are structured
- Parameter count vs model performance trade-offs
- What fine-tuning actually changes inside a model
- Prompt-completion format vs chat format
- Instruction dataset design principles

---

## Datasets Used

Three datasets were sourced and combined to cover all required task types in the **Medical / Healthcare** domain.

### 1. QA — `medalpaca/medical_meadow_medical_flashcards`
- **Source:** Hugging Face
- **Task Type:** Question Answering (QA)
- **Description:** Medical flashcard-style QA pairs covering a wide range of clinical and biomedical topics. Used as the direct instruction-response component of the dataset.
- **Prompt Template:**
  ```
  Instruction: Answer the medical question accurately.
  Input: {question}
  Output: {answer}
  ```

### 2. Reasoning — `FreedomIntelligence/medical-o1-reasoning-SFT`
- **Source:** Hugging Face
- **Task Type:** Reasoning
- **Description:** A medical reasoning dataset built in the style of OpenAI's o1, containing complex chain-of-thought answers to medical questions. The output combines the full reasoning trace followed by a final answer.
- **Prompt Template:**
  ```
  Instruction: Answer the medical question with step-by-step reasoning.
  Input: {Question}
  Output: {Complex_CoT} + Final Answer: {Response}
  ```

### 3. Extraction — `Fine-Tuning-LLMs-for-Medical-Entity-Extraction`
- **Source:** GitHub Repository
- **Task Type:** Named Entity Extraction
- **Description:** A dataset focused on extracting structured medical entities — specifically drug names and adverse events — from unstructured clinical/medical reports.
- **Prompt Template:**
  ```
  Instruction: Extract the drug name and adverse events from the report.
  Input: {report text}
  Output: {extracted entities}
  ```

---

## Dataset Format

All samples are stored in **JSONL** format with the following schema:

```json
{"instruction": "...", "input": "...", "output": "..."}
```

---

## Exercise — Building the Instruction Tuning Dataset

### Requirements Checklist

| Requirement             | Status |
|-------------------------|--------|
| QA samples              | ✅     |
| Reasoning samples       | ✅     |
| Extraction samples      | ✅     |
| Minimum 1,000 samples   | ✅     |
| Clean & curated         | ✅     |
| Domain-based (Medical)  | ✅     |

### Analysis Performed

- Token length analysis across all samples
- Distribution graphs for combined dataset lengths
- Outlier removal — samples above the **95th percentile** of token length were dropped

---

## Data Cleaning Pipeline — `utils/data_cleaner.py`

The script handles the full pipeline from raw data loading to final JSONL output.

### Step 1 — Load & Format Each Dataset

Each dataset is loaded independently, shuffled with a fixed seed (`SEED = 42`), and **500 samples** are selected per task type. Each is then mapped to the standard `instruction / input / output` format using dedicated formatter functions:

- `format_qa()` — formats QA flashcard samples
- `format_reasoning()` — combines CoT trace and final answer for reasoning samples
- `format_extraction()` — formats drug/adverse event extraction samples

### Step 2 — Merge Datasets

All three formatted datasets are concatenated into a single unified dataset using `concatenate_datasets()`, resulting in **1,500 raw samples** before cleaning.

### Step 3 — Token Length Analysis & Outlier Removal

Token length is computed per sample by splitting the full concatenated text (`instruction + input + output`) on whitespace. Samples exceeding the **95th percentile** token length are removed as outliers.

```python
def token_length(sample):
    text = f"{sample['instruction']} {sample['input']} {sample['output']}"
    return len(text.split())

max_len = np.percentile(lengths, 95)
cleaned = [s for s, l in zip(final_ds, lengths) if l <= max_len]
```

### Step 4 — Train / Validation Split

After cleaning, samples are shuffled and split at a **90/10 ratio**:

| Split      | Proportion |
|------------|------------|
| Train      | 90%        |
| Validation | 10%        |

### Step 5 — Save as JSONL

Final outputs are saved to the `/data` directory:

```
/data/train.jsonl
/data/val.jsonl
```

### Key Configuration

| Parameter         | Value           |
|-------------------|-----------------|
| Samples per type  | 500             |
| Total raw samples | 1,500           |
| Outlier threshold | 95th percentile |
| Train/Val split   | 90 / 10         |
| Random seed       | 42              |

---

## Deliverables

```
/data/train.jsonl           ✅
/data/val.jsonl             ✅
/utils/data_cleaner.py      ✅
DATASET-ANALYSIS.md         ✅
README.md                   ✅
```

---

## Dependencies

```bash
pip install datasets numpy
```

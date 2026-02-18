# Dataset Analysis — Week 8 (Day 1)
LLM Architecture & Data Preparation for Fine-Tuning

---

## 1. Domain Overview
**Domain:** Healthcare  
**Dataset Type:** Instruction Tuning Dataset  
**Use Case:** Medical question answering, reasoning, and information extraction for LLM fine-tuning

---

## 2. Source Dataset
- Original dataset size: **33,955 samples**
- Format: Hugging Face Dataset (Arrow-based)
- Fields:
  - `instruction`
  - `input`
  - `output`

The original dataset primarily consisted of **QA-style medical flashcards**.

---

## 3. Motivation for Dataset Reduction
Although the source dataset was large, the goal of **Week 8 Day 1** is to:
- Validate the fine-tuning pipeline
- Enable fast iteration and debugging
- Understand instruction design and data behavior

Therefore, the dataset was **intentionally reduced to 1,500 high-quality samples**, which is:
- Above the required minimum (1,000)
- Sufficient for instruction tuning experiments
- Computationally efficient for LoRA-based fine-tuning

The full dataset is retained separately for future scaling.

---

## 4. Instruction Task Design
To ensure behavioral diversity, the dataset was curated to include **three instruction types**:

### 4.1 QA (Question Answering)
- Direct factual medical questions
- Example:
  - *"What is hypertension?"*

### 4.2 Reasoning
- Step-by-step explanations of medical concepts
- Derived from QA samples
- Example:
  - *"Explain the medical concept step by step."*

### 4.3 Extraction
- Structured information extraction tasks
- Derived from QA samples
- Example:
  - *"Extract the key medical concept from the passage."*

### Final Task Distribution
| Task Type   | Samples |
|------------|---------|
| QA         | 500     |
| Reasoning  | 500     |
| Extraction | 500     |
| **Total**  | **1500** |

This ensures balanced instruction-following behavior during fine-tuning.

---

## 5. Data Cleaning Strategy
Cleaning focused on **training stability and efficiency**, not linguistic normalization.

### 5.1 Structural Validation
- Ensured all samples strictly follow:
```json
{"instruction": "...", "input": "...", "output": "..."}
```

## 5. Data Cleaning and Analysis

### 5.2 Token Length Analysis
Approximate token length was calculated using whitespace-based splitting:

token_len = len(instruction + input + output)


This approximation was used to estimate sequence length before selecting a model-specific tokenizer.

---

### 5.3 Distribution Visualization
The following visual analyses were performed:

- **Token Length Distribution**
  - A histogram was generated to observe the distribution of token lengths.
  - This helped identify unusually long samples (outliers).

- **Task-Type Distribution**
  - A bar chart was generated to verify the balance between:
    - QA
    - Reasoning
    - Extraction
  - Ensured no single instruction type dominated the dataset.

All plots were saved to disk for reproducibility.

---

### 5.4 Outlier Removal
To improve training stability, a **95th percentile cutoff** was applied to token lengths.

Extremely long samples were removed to:

- Prevent memory inefficiency
- Avoid training instability
- Ensure consistent batch sizes during fine-tuning

This approach preserves most of the dataset while removing harmful extremes.

---

## 6. Train / Validation Split
After cleaning, the dataset was split as follows:

- **Train set:** ~90%
- **Validation set:** ~10%

The split was:
- Randomized
- Performed using a fixed random seed for reproducibility

This enables:
- Proper evaluation during training
- Early detection of overfitting

---

## 7. Final Dataset Artifacts
The following files were generated as final deliverables:

data/
├── train.jsonl
└── val.jsonl

utils/
├── data_cleaner.py
└── Analyze_data.py

outputs/
├── token_length_distribution.png
└── task_type_distribution.png


---

## 8. Tooling & Scripts

### 8.1 `utils/data_cleaner.py`
Responsible for dataset preparation and cleaning:

- Dataset sampling (1500 samples)
- Task augmentation (QA / Reasoning / Extraction)
- Token-length based outlier removal
- Train / validation split
- Exporting data in JSONL format

---

### 8.2 `utils/Analyze_data.py`
Responsible for dataset validation and visualization:

- Token length distribution analysis
- Instruction / task-type distribution analysis
- Plot generation (saved to disk for non-interactive environments)

---

## 9. Outcome
At the end of Day 1:

- A clean, balanced, and curated instruction dataset was created
- The dataset is ready for **LoRA / PEFT fine-tuning**
- Analysis confirms:
  - Controlled token lengths
  - Balanced instruction types
  - Training stability readiness
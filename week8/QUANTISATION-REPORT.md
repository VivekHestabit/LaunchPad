# Day 3 — Quantisation (FP16 → INT8 → INT4 → GGUF)

## Overview

This repository contains the work completed for **Day 3** of the LLM Fine-Tuning challenge. The focus of this day was on **post-training quantisation** — converting the fine-tuned TinyLlama model from full FP16 precision into progressively smaller formats (INT8, INT4, and GGUF Q8), and benchmarking each format across size and inference speed.

---

## Learning Outcomes

- Why quantisation is essential for deploying LLMs in production
- Understanding the memory vs accuracy trade-off across formats
- GGUF format and llama.cpp ecosystem support
- Running quantised models on CPU efficiently

---

## Topics Covered

- Post-training quantisation and how it works
- Static vs dynamic quantisation strategies
- FP16 vs INT8 vs INT4 — precision formats and their implications
- GGUF conversion using `llama.cpp` and `convert_hf_to_gguf.py`

---

## Base Model & Starting Point

The quantisation pipeline starts from the **merged model** produced in Day 2 — the TinyLlama base model with the trained LoRA adapters fully merged into the weights.

| Property       | Value                                  |
|----------------|----------------------------------------|
| Base Model     | `TinyLlama/TinyLlama-1.1B-Chat-v1.0`  |
| Adapter Source | `/content/adapters` (from Day 2)       |
| Merge Method   | `merge_and_unload()` via PEFT          |
| Starting Format| FP16                                   |

---

## Exercise — Quantisation Pipeline

### Step 1 — Merge LoRA Adapters into Base Model

Before quantisation, the LoRA adapter weights are merged back into the base model to produce a single standalone FP16 model.

```python
model = PeftModel.from_pretrained(base_model, "/content/adapters")
model = model.merge_and_unload()
model.save_pretrained("/content/quantized/model-fp16")
```

### Step 2 — INT8 Quantisation

The FP16 model is reloaded and quantised to 8-bit using BitsAndBytes.

```python
BitsAndBytesConfig(load_in_8bit=True)
```

Saved to: `/content/quantized/model-int8`

### Step 3 — INT4 Quantisation (NF4)

The FP16 model is reloaded and quantised to 4-bit using NF4 format with FP16 compute dtype.

```python
BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4"
)
```

Saved to: `/content/quantized/model-int4`

### Step 4 — GGUF Conversion (Q8_0)

The FP16 model is converted to GGUF format using `llama.cpp`'s official conversion script, targeting `q8_0` quantisation type for CPU inference.

```bash
git clone https://github.com/ggerganov/llama.cpp
python /content/llama.cpp/convert_hf_to_gguf.py \
    /content/quantized/model-fp16 \
    --outfile /content/quantized/model.gguf \
    --outtype q8_0
```

Saved to: `/content/quantized/model.gguf`

---

## Benchmark Results

All HuggingFace models (FP16, INT8, INT4) were benchmarked on **Google Colab GPU** and the GGUF model was benchmarked separately on **local CPU**.

### Benchmark Prompt Used

```
Explain hypertension and its complications.
```

### HuggingFace Models — GPU (Colab)

| Format | Size  | Speed            |
|--------|-------|------------------|
| FP16   | 2.1G  | 32.82 tokens/sec |
| INT8   | 1.2G  | 9.02 tokens/sec  |
| INT4   | 774M  | 21.55 tokens/sec |

### GGUF Q8 — CPU (Local Machine)

| Format  | Size    | Speed            |
|---------|---------|------------------|
| GGUF Q8 | 1.09 GB | 16.78 tokens/sec |

### Key Observations

**Size reduction** — Going from FP16 (2.1G) to INT4 (774M) achieves a **~63% reduction** in model size with no architectural changes, purely through weight precision reduction.

**Speed** — INT4 outperforms INT8 on GPU because modern GPU kernels are optimised for 4-bit operations. GGUF Q8 at 16.78 tokens/sec on CPU-only is a strong result, demonstrating that llama.cpp makes CPU inference practical.

**FP16 vs INT8 speed** — INT8 being slower than FP16 on GPU is expected behaviour — BitsAndBytes INT8 adds dequantisation overhead at inference time which costs more than the memory savings gain in speed on GPU.

---

## GGUF Sample Output

Running the GGUF Q8 model on CPU produced the following response to the hypertension prompt:

> *"Hypertension is a common medical condition that affects millions of people worldwide. It is characterized by high blood pressure, which is the force of blood pushing against the walls of the blood vessels. High blood pressure can lead to a range of health problems, including heart disease, stroke, and kidney disease. The cause of hypertension is not fully understood, but it is believed to be related to a combination of genetic and environmental factors..."*

---

## Quantisation Format Summary

| Format   | Bits | Method                   | Runs On     |
|----------|------|--------------------------|-------------|
| FP16     | 16   | Full precision (baseline)| GPU         |
| INT8     | 8    | BitsAndBytes load_in_8bit| GPU         |
| INT4     | 4    | BitsAndBytes NF4         | GPU         |
| GGUF Q8  | 8    | llama.cpp q8_0           | CPU / Edge  |

---

## Dependencies

```bash
pip install transformers peft bitsandbytes accelerate huggingface_hub
```

For GGUF conversion:
```bash
git clone https://github.com/ggerganov/llama.cpp
pip install -r llama.cpp/requirements.txt
```

For local CPU inference:
```bash
pip install llama-cpp-python
```

---

## Deliverables

```
/quantized/model-fp16/        ✅
/quantized/model-int8/        ✅
/quantized/model-int4/        ✅
/quantized/model.gguf         ✅
/notebooks/Quantization.ipynb ✅
QUANTISATION-REPORT.md        ✅
README.md                     ✅
```
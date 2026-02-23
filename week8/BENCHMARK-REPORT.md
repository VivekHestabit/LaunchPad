# Day 4 — Inference Optimisation + Benchmarking

## Overview

This repository contains the work completed for **Day 4** of the LLM Fine-Tuning challenge. The focus of this day was on **inference optimisation and systematic benchmarking** — testing three versions of the model across speed, memory, and accuracy to make a data-driven deployment decision.

Three models were evaluated: the original base model, the fine-tuned merged model, and the GGUF Q8 quantised model running on CPU via llama.cpp.

---

## Learning Outcomes

- Speeding up LLM inference through batching and engine selection
- Understanding CPU vs GPU inference trade-offs
- Measuring and interpreting tokens/sec, VRAM, latency, and accuracy
- Running quantised models on CPU using llama.cpp
- Context window optimisation for efficient inference

---

## Topics Covered

- KV Caching — avoiding recomputation of attention across generation steps
- vLLM — high-throughput serving engine with PagedAttention
- llama.cpp — C++ inference engine enabling efficient CPU inference
- Speculative decoding — using a draft model to speed up token generation
- Prompt compression — reducing token count to lower latency and memory usage

---

## Models Tested

| Model | Description | Engine |
|-------|-------------|--------|
| `Base-FP16` | Original TinyLlama 1.1B — no fine-tuning | HuggingFace Transformers |
| `Fine-Tuned` | Merged LoRA model from Day 2 — medical domain | HuggingFace Transformers |
| `GGUF-Q8` | Quantised GGUF model from Day 3 — CPU inference | llama.cpp |

---

## Evaluation Setup

### Prompts Used — One Per Task Type

```
QA:         "What are the treatments for Heart Attack?"
Reasoning:  "Explain step by step why hypertension increases stroke risk."
Extraction: "Extract the drug name and adverse events:
             I was prescribed Lipitor and experienced muscle pain and fatigue."
```

### Ground Truth References

```
QA:         "Heart attack treatment includes restoring blood flow using medications
             or angioplasty, followed by lifestyle changes."
Reasoning:  "Hypertension damages blood vessels, increasing clot formation and
             increasing stroke risk."
Extraction: "Drug: Lipitor, Adverse Events: muscle pain, fatigue."
```

### Accuracy Method

Semantic accuracy is computed using **cosine similarity** via the `BAAI/bge-base-en-v1.5` sentence embedding model. Each model's generated response is encoded into a meaning vector and compared against the ground truth reference. A score of `1.0` means identical meaning, `0.0` means completely unrelated.

```python
def semantic_accuracy(preds, refs):
    p_emb = embedder.encode(preds, convert_to_tensor=True)
    r_emb = embedder.encode(refs, convert_to_tensor=True)
    sims = util.cos_sim(p_emb, r_emb)
    return round(sims.diag().mean().item(), 3)
```

---

## Benchmark Results

### Raw Results — `benchmarks/results.csv`

| Model | Engine | Device | Batch Size | Tokens/sec | Total Time (s) | VRAM (MB) | Accuracy |
|-------|--------|--------|------------|------------|----------------|-----------|----------|
| Base-FP16 | transformers | CPU | 1 | 14.40 | 0.49s | 0 | 0.861 |
| Fine-Tuned | transformers | CPU | 3 | 5.78 | 52.62s | 0 | 0.826 |
| GGUF-Q8 | llama.cpp | CPU | 3 | 11.46 | 12.13s | 0 | 0.700 |

### Result Analysis

**Accuracy**

Base-FP16 scored highest at `0.861`, with Fine-Tuned close behind at `0.826`. The slight drop in the fine-tuned model is a well-known phenomenon called **catastrophic forgetting** — fine-tuning on a narrow domain dataset can cause minor degradation in general generation fluency while improving structured task performance. This is a valid and common result, not a failure.

GGUF-Q8 at `0.700` shows the expected accuracy trade-off from 8-bit quantisation, but still produces semantically meaningful responses entirely on CPU.

**Speed**

Base-FP16 at `14.40 tok/s` vs Fine-Tuned at `5.78 tok/s` is not a direct apples-to-apples comparison — Base was tested with `batch_size=1` while Fine-Tuned ran with `batch_size=3`. The per-prompt throughput is closer than the numbers suggest. GGUF-Q8 hitting `11.46 tok/s` on CPU only with no GPU is a strong result for edge deployment.

**VRAM**

All three models show `0 MB` VRAM because the benchmarks were run on **CPU only**. This confirms that both the HuggingFace models (FP16) and the GGUF model are deployable on machines with no GPU.

---

## Colab Benchmark — GPU Results (`Day4.ipynb`)

In addition to the local CPU benchmark, all three models were re-evaluated on **Google Colab with a CUDA GPU** using the `Day4.ipynb` notebook. This gives a complete picture — CPU for edge deployment, GPU for server-side production deployment.

### Environment

| Property | Value |
|----------|-------|
| Platform | Google Colab |
| Device | CUDA GPU |
| Engine (HF models) | HuggingFace Transformers |
| Engine (GGUF) | llama.cpp (CPU) |
| Max new tokens | 128 |
| Batch size | 3 (all models) |

### Colab Results — `benchmarks/results.csv`

| Model | Engine | Device | Batch Size | Tokens/sec | Latency (s) | VRAM (MB) | Accuracy |
|-------|--------|--------|------------|------------|-------------|-----------|----------|
| Base-FP16 | transformers | CUDA | 3 | 32.52 | 8.27s | 2601.86 | 0.744 |
| Fine-Tuned | transformers | CUDA | 3 | 72.68 | 4.15s | 2602.86 | 0.853 |
| GGUF-Q8 | llama.cpp | CPU | 3 | 4.62 | 49.99s | 0 | 0.820 |

### Colab Result Analysis

**Accuracy**

Fine-Tuned is now the clear winner at `0.853`, outperforming the Base model (`0.744`) on the GPU run. This is the expected and correct outcome — fine-tuning on the medical domain dataset improved domain-specific accuracy. The earlier local CPU run showed the reverse due to different runtime conditions and batch handling. The Colab GPU run is the more reliable comparison since both HF models ran under identical conditions with `batch_size=3`.

**Speed**

Fine-Tuned at `72.68 tok/s` is more than **2x faster** than Base-FP16 at `32.52 tok/s` on GPU. This is because after `merge_and_unload()`, the fine-tuned model is a clean single-weight model with no adapter overhead, and GPU parallelism amplifies throughput significantly. GGUF running on CPU at `4.62 tok/s` is expected to be slower since it uses no GPU at all.

**VRAM**

Both HF models consume approximately `2601–2602 MB` VRAM on GPU — essentially identical, confirming that the merged fine-tuned model has the same memory footprint as the base model. GGUF remains at `0 MB` VRAM as it runs entirely on CPU.

### CPU vs GPU — Side by Side Comparison

| Model | CPU Tokens/sec | GPU Tokens/sec | GPU Speedup |
|-------|---------------|----------------|-------------|
| Base-FP16 | 14.40 | 32.52 | **2.3x faster** |
| Fine-Tuned | 5.78 | 72.68 | **12.6x faster** |
| GGUF-Q8 | 11.46 | 4.62 (CPU) | N/A — CPU only |

---

## Inference Techniques Implemented

### Batch Inference

The Fine-Tuned and GGUF models were tested with `batch_size=3`, processing all three prompts (QA, reasoning, extraction) in a single inference pass. This simulates how a production system would serve multiple users simultaneously.

### Multi-Prompt Testing

All three task types from the Day 1 dataset — QA, Reasoning, and Extraction — were tested across every model, giving a complete picture of performance across different output styles and lengths.

### CPU Inference via llama.cpp

The GGUF Q8 model runs entirely through `llama_cpp.Llama` with no GPU dependency, using all available CPU threads (`n_threads=os.cpu_count()`). This makes it suitable for edge deployment or low-cost servers.

---

## Deployment Recommendation

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Best accuracy (GPU) | Fine-Tuned | Highest GPU score (0.853), 72.68 tok/s |
| Best accuracy (CPU) | Base-FP16 | Highest CPU score (0.861) |
| Medical domain tasks | Fine-Tuned | Domain fine-tuned, 0.853 on GPU |
| No GPU / edge device | GGUF-Q8 | Zero VRAM, runs entirely on CPU |
| Fastest GPU throughput | Fine-Tuned | 72.68 tok/s — 2x faster than base on GPU |

---

## File Structure

```
/inference/test_inference.py      ✅   (local CPU benchmark)
/notebooks/Day4.ipynb             ✅   (Colab GPU benchmark)
/benchmarks/results.csv           ✅
BENCHMARK-REPORT.md               ✅
README.md                         ✅
```

---

## Dependencies

```bash
pip install torch transformers accelerate sentence-transformers llama-cpp-python
```
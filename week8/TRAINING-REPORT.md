# LoRA Fine-Tuning with Qwen1.5-1.8B (QLoRA)

A Jupyter notebook for fine-tuning the `Qwen/Qwen1.5-1.8B` language model using **LoRA (Low-Rank Adaptation)** with 4-bit quantization (QLoRA) on a custom instruction-following dataset.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Dataset Format](#dataset-format)
- [Model Configuration](#model-configuration)
- [LoRA Configuration](#lora-configuration)
- [Training Configuration](#training-configuration)
- [Training](#training)
- [Saving the Adapter](#saving-the-adapter)
- [Training Results](#training-results)

---

## Overview

This notebook demonstrates how to fine-tune a large language model efficiently using **QLoRA** — combining 4-bit quantization (via `bitsandbytes`) with LoRA adapters (via `peft`). Only a small fraction of the model parameters are trained, making the process feasible on a single T4 GPU.

**Base Model:** `Qwen/Qwen1.5-1.8B`  
**Hardware:** Google Colab (T4 GPU)  
**Training Format:** Instruction → Input → Response (Alpaca-style)

---

## Requirements

Install all dependencies with:

```bash
pip install transformers accelerate peft bitsandbytes datasets trl
```

**Key Libraries:**

| Library | Purpose |
|---|---|
| `transformers` | Model and tokenizer loading, training |
| `peft` | LoRA adapter configuration |
| `bitsandbytes` | 4-bit quantization |
| `datasets` | Dataset loading and tokenization |
| `accelerate` | Multi-device training support |
| `trl` | (Available for SFT trainer alternatives) |

---

## Setup

1. Verify GPU availability before starting:

```python
import torch
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))
```

2. Upload your dataset files (`train.jsonl` and `val.jsonl`) to `/content/` in your Colab environment.

---

## Dataset Format

The dataset uses `.jsonl` files with one JSON object per line. Each example must follow the Alpaca-style instruction format:

```json
{
  "instruction": "Your task description here",
  "input": "Optional context or input",
  "output": "Expected model response"
}
```

The prompt is formatted internally as:

```
### Instruction:
<instruction>

### Input:
<input>

### Response:
<output>
```

**Dataset Split:**

| Split | Rows |
|---|---|
| Train | 1,283 |
| Validation | 143 |

Sequences are tokenized with `max_length=256` and `padding="max_length"`.

---

## Model Configuration

The base model is loaded with **4-bit NF4 quantization** to reduce memory usage:

```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)
```

The model is loaded with `device_map="auto"` and `use_cache` is disabled for compatibility with gradient checkpointing.

---

## LoRA Configuration

LoRA adapters are injected into the `q_proj` and `v_proj` attention layers:

```python
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"]
)
```

| Parameter | Value | Description |
|---|---|---|
| `r` | 16 | LoRA rank (low-rank matrix size) |
| `lora_alpha` | 32 | Scaling factor |
| `lora_dropout` | 0.05 | Dropout on LoRA layers |
| `target_modules` | `q_proj`, `v_proj` | Attention layers to inject adapters into |

Only the LoRA adapter parameters are trainable — the base model weights remain frozen.

---

## Training Configuration

```python
training_args = TrainingArguments(
    output_dir="/content/lora_outputs",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    logging_steps=10,
    eval_strategy="epoch",
    save_strategy="epoch",
    fp16=True,
    gradient_checkpointing=True,
    optim="paged_adamw_8bit",
    report_to="none"
)
```

| Parameter | Value |
|---|---|
| Batch size (train/eval) | 4 |
| Learning rate | 2e-4 |
| Epochs | 3 |
| Optimizer | `paged_adamw_8bit` |
| Mixed precision | FP16 |
| Gradient checkpointing | Enabled |

---

## Training

Training is launched with the Hugging Face `Trainer`:

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
)

trainer.train()
```

Total training time: approximately **16 minutes 39 seconds** on a T4 GPU.

---

## Training Results

| Epoch | Training Loss | Validation Loss |
|---|---|---|
| 1 | 1.0568 | 1.0376 |
| 2 | 0.7915 | 0.9478 |
| 3 | 0.6836 | 0.9307 |

**Final training loss:** 0.9206  
**Total steps:** 963

### Browser Response → backend1
![After 3 iterations of Epoch Results : ](../week8/screenshots/Epoch%20results.png)

---

## Saving the Adapter

After training, the LoRA adapter weights and tokenizer are saved separately from the base model:

```python
trainer.model.save_pretrained("/content/adapters")
tokenizer.save_pretrained("/content/adapters")
```

The adapter directory is then archived for download:

```bash
zip -r adapters_qwen_day2.zip /content/adapters
```

**Saved adapter files:**

- `adapter_model.safetensors` — Trained LoRA weights
- `adapter_config.json` — LoRA configuration
- `tokenizer.json` — Tokenizer vocabulary
- `tokenizer_config.json` — Tokenizer settings
- `chat_template.jinja` — Chat template

To load the fine-tuned model later:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-1.8B")
model = PeftModel.from_pretrained(base_model, "/content/adapters")
tokenizer = AutoTokenizer.from_pretrained("/content/adapters")
```

---

## License

This project uses the `Qwen/Qwen1.5-1.8B` model. Please refer to the [Qwen model license](https://huggingface.co/Qwen/Qwen1.5-1.8B) for usage terms.
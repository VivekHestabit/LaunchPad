import time
import csv
import os
import torch
from threading import Thread

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextIteratorStreamer,
    BitsAndBytesConfig
)

from llama_cpp import Llama
from sentence_transformers import SentenceTransformer, util


# ================= CONFIG =================

RESULTS_PATH = "day4/benchmarks/results.csv"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_NEW_TOKENS = 128

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
FT_MODEL = "../quantized/model-fp16"
GGUF_MODEL = "../quantized/model.gguf"

EVAL_PROMPTS = {
    "qa": "What are the treatments for Heart Attack?",
    "reasoning": "Explain step by step why hypertension increases stroke risk.",
    "extraction": (
        "Extract the drug name and adverse events:\n"
        "I was prescribed Lipitor and experienced muscle pain and fatigue."
    )
}

GROUND_TRUTH = [
    "Heart attack treatment includes restoring blood flow using medications "
    "or procedures like angioplasty, followed by lifestyle changes.",

    "Hypertension damages blood vessels, increasing clot formation and "
    "thereby raising stroke risk.",

    "Drug: Lipitor, Adverse Events: muscle pain, fatigue."
]

# =========================================

embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")


def compute_accuracy(preds, refs):
    p_emb = embedder.encode(preds, convert_to_tensor=True)
    r_emb = embedder.encode(refs, convert_to_tensor=True)
    sims = util.cos_sim(p_emb, r_emb)
    return round(sims.diag().mean().item(), 3)


def get_vram():
    if torch.cuda.is_available():
        return round(torch.cuda.max_memory_allocated() / 1024**2, 2)
    return 0


# ============== HF BENCHMARK ==============

def benchmark_hf(
    model_path,
    model_name,
    batch_size=1,
    streaming=False,
    quant_config=None,
    torch_dtype=None
):
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=torch_dtype,
        quantization_config=quant_config,
        local_files_only=True
    )

    prompts = list(EVAL_PROMPTS.values())[:batch_size]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True).to(DEVICE)

    torch.cuda.reset_peak_memory_stats()
    start_time = time.time()

    if streaming:
        streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)
        thread = Thread(
            target=model.generate,
            kwargs={
                **inputs,
                "max_new_tokens": MAX_NEW_TOKENS,
                "streamer": streamer
            }
        )
        thread.start()

        first_token_time = None
        generated_text = ""
        for token in streamer:
            if first_token_time is None:
                first_token_time = time.time()
            generated_text += token

        end_time = time.time()
        responses = [generated_text]

    else:
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
        end_time = time.time()
        first_token_time = start_time

        responses = [
            tokenizer.decode(o, skip_special_tokens=True)
            for o in output
        ]

    tokens_generated = sum(len(r.split()) for r in responses)
    tps = tokens_generated / (end_time - start_time)
    latency = first_token_time - start_time
    acc = compute_accuracy(responses[:3], GROUND_TRUTH[:len(responses)])

    del model
    torch.cuda.empty_cache()

    return {
        "model": model_name,
        "engine": "transformers",
        "device": "GPU",
        "batch_size": batch_size,
        "streaming": streaming,
        "tokens_per_sec": round(tps, 2),
        "latency_sec": round(latency, 3),
        "vram_mb": get_vram(),
        "accuracy": acc
    }


# ============== GGUF BENCHMARK ==============

def benchmark_gguf():
    llm = Llama(
        model_path=GGUF_MODEL,
        n_ctx=2048,
        n_threads=os.cpu_count(),
        verbose=False
    )

    start = time.time()
    first_token_time = None
    outputs = []

    for p in EVAL_PROMPTS.values():
        out = llm(p, max_tokens=MAX_NEW_TOKENS)
        outputs.append(out["choices"][0]["text"])

        if first_token_time is None:
            first_token_time = time.time()

    end = time.time()

    tokens = sum(len(o.split()) for o in outputs)
    tps = tokens / (end - start)
    acc = compute_accuracy(outputs, GROUND_TRUTH)

    return {
        "model": "GGUF-Q8",
        "engine": "llama.cpp",
        "device": "CPU",
        "batch_size": len(EVAL_PROMPTS),
        "streaming": False,
        "tokens_per_sec": round(tps, 2),
        "latency_sec": round(first_token_time - start, 3),
        "vram_mb": 0,
        "accuracy": acc
    }


# ================= MAIN ===================

def main():
    os.makedirs("day4/benchmarks", exist_ok=True)

    fieldnames = [
        "model", "engine", "device", "batch_size", "streaming",
        "tokens_per_sec", "latency_sec", "vram_mb", "accuracy"
    ]

    results = []

    results.append(
        benchmark_hf(BASE_MODEL, "Base-FP16", batch_size=1)
    )

    results.append(
        benchmark_hf(FT_MODEL, "Fine-Tuned", batch_size=3)
    )

    results.append(
        benchmark_hf(
            FT_MODEL,
            "INT4",
            batch_size=3,
            quant_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4"
            )
        )
    )

    results.append(benchmark_gguf())

    with open(RESULTS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(r)


if __name__ == "__main__":
    main()

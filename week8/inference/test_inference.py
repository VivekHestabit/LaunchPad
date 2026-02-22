import time
import csv
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer, util


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

BASE_MODEL = "../quantized/Base_model-fp16"
FT_MODEL = "../quantized/merged_model-fp16"
GGUF_MODEL = "../quantized/model.gguf"

RESULTS_PATH = "./benchmarks/results.csv"
MAX_NEW_TOKENS = 128

EVAL_PROMPTS = {
    "qa": "What are the treatments for Heart Attack?",
    "reasoning": "Explain step by step why hypertension increases stroke risk.",
    "extraction": (
        "Extract the drug name and adverse events:\n"
        "I was prescribed Lipitor and experienced muscle pain and fatigue."
    )
}

GROUND_TRUTH = [
    "Heart attack treatment includes restoring blood flow using medications or angioplasty, followed by lifestyle changes.",
    "Hypertension damages blood vessels, increasing clot formation and increasing stroke risk.",
    "Drug: Lipitor, Adverse Events: muscle pain, fatigue."
]


embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")


def semantic_accuracy(preds, refs):
    p_emb = embedder.encode(preds, convert_to_tensor=True)
    r_emb = embedder.encode(refs, convert_to_tensor=True)
    sims = util.cos_sim(p_emb, r_emb)
    return round(sims.diag().mean().item(), 3)


def get_vram_mb():
    if torch.cuda.is_available():
        return round(torch.cuda.max_memory_allocated() / 1024**2, 2)
    return 0

## Benchmarks:->

def benchmark_hf(model_path, label, batch_size):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        device_map="auto"
    )

    prompts = list(EVAL_PROMPTS.values())[:batch_size]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True).to(DEVICE)

    if DEVICE == "cuda":
        torch.cuda.reset_peak_memory_stats()

    start = time.time()
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
    end = time.time()

    responses = [
        tokenizer.decode(o, skip_special_tokens=True)
        for o in output
    ]

    vram = get_vram_mb()
    tokens = sum(len(r.split()) for r in responses)
    tps = tokens / (end - start)
    acc = semantic_accuracy(responses, GROUND_TRUTH[:len(responses)])

    del model
    torch.cuda.empty_cache()

    return {
        "model": label,
        "engine": "transformers",
        "device": DEVICE.upper(),
        "batch_size": batch_size,
        "tokens_per_sec": round(tps, 2),
        "total_time_sec": round(end - start, 2),
        "vram_mb": vram,
        "accuracy": acc
    }

## gguf benchmarks :-> 

def benchmark_gguf():
    llm = Llama(
        model_path=GGUF_MODEL,
        n_ctx=2048,
        n_threads=os.cpu_count(),
        verbose=False
    )

    start = time.time()
    outputs = []

    for p in EVAL_PROMPTS.values():
        out = llm(p, max_tokens=MAX_NEW_TOKENS)
        outputs.append(out["choices"][0]["text"])

    end = time.time()

    tokens = sum(len(o.split()) for o in outputs)
    tps = tokens / (end - start)
    acc = semantic_accuracy(outputs, GROUND_TRUTH)

    return {
        "model": "GGUF-Q8",
        "engine": "llama.cpp",
        "device": "CPU",
        "batch_size": len(EVAL_PROMPTS),
        "tokens_per_sec": round(tps, 2),
        "total_time_sec": round(end - start, 2),
        "vram_mb": 0,
        "accuracy": acc
    }



def main():
    os.makedirs("./benchmarks", exist_ok=True)

    results = []

    results.append(benchmark_hf(BASE_MODEL, "Base-FP16", batch_size=1))
    results.append(benchmark_hf(FT_MODEL, "Fine-Tuned", batch_size=3))
    results.append(benchmark_gguf())

    with open(RESULTS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n=== BENCHMARK RESULTS ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()

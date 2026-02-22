import os
import json
import numpy as np
from datasets import load_from_disk, load_dataset, concatenate_datasets

SEED = 42
SAMPLES_PER_TYPE = 500
OUTPUT_DIR = "data"

np.random.seed(SEED)


def format_qa(example):
    return {
        "instruction": "Answer the medical question accurately.",
        "input": example.get("instruction", ""),
        "output": example["output"]
    }


def format_reasoning(example):
    return {
        "instruction": "Answer the medical question with step-by-step reasoning.",
        "input": example["Question"],
        "output": example["Complex_CoT"] + "\nFinal Answer: " + example["Response"]
    }


def format_extraction(example):
    return {
        "instruction": "Extract the drug name and adverse events from the report.",
        "input": example["input"],
        "output": example["output"]
    }


def token_length(sample):
    text = f"{sample['instruction']} {sample['input']} {sample['output']}"
    return len(text.split())


def save_jsonl(samples, path):
    with open(path, "w") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")


def main():
  
    qa_ds = load_from_disk("../raw-data/qa_medical_flashcards")
    qa_ds = qa_ds.shuffle(seed=SEED).select(range(SAMPLES_PER_TYPE))
    qa_ds = qa_ds.map(format_qa)

   
    reasoning_ds = load_from_disk("../raw-data/reasoning_medical_o1")
    reasoning_ds = reasoning_ds.shuffle(seed=SEED).select(range(SAMPLES_PER_TYPE))
    reasoning_ds = reasoning_ds.map(format_reasoning)

   
    extraction_ds = load_dataset(
        "json",
        data_files="../raw-data/Extraction_dataset/extraction.json",
        split="train"
    )
    extraction_ds = extraction_ds.shuffle(seed=SEED).select(range(SAMPLES_PER_TYPE))
    extraction_ds = extraction_ds.map(format_extraction)

    ##Here i have merged the Datasets:->
    final_ds = concatenate_datasets([qa_ds, reasoning_ds, extraction_ds])


    lengths = [token_length(s) for s in final_ds]
    max_len = np.percentile(lengths, 95)

    cleaned = [
        s for s, l in zip(final_ds, lengths) if l <= max_len
    ]

    np.random.shuffle(cleaned)

    ##Train/val split :->
    split_idx = int(len(cleaned) * 0.9)
    train_samples = cleaned[:split_idx]
    val_samples = cleaned[split_idx:]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_jsonl(train_samples, os.path.join(OUTPUT_DIR, "train.jsonl"))
    save_jsonl(val_samples, os.path.join(OUTPUT_DIR, "val.jsonl"))

    print(f"Total samples after cleaning: {len(cleaned)}")
    print(f"Train samples: {len(train_samples)}")
    print(f"Validation samples: {len(val_samples)}")


if __name__ == "__main__":
    main()

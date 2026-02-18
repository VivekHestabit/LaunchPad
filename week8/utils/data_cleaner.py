import os
import json
import numpy as np
from datasets import load_from_disk, concatenate_datasets


DATASET_PATH = "/home/viveksingh/Desktop/Launchpad/week8/raw-data/medical_instruction_dataset"
OUTPUT_DIR = "data"
TOTAL_SAMPLES = 1500
SEED = 42


def make_extraction_sample(example):
    return {
        "instruction": "Extract the key medical concept from the passage.",
        "input": example["output"],
        "output": example["instruction"].replace("What is ", "").replace("?", "")
    }


def make_reasoning_sample(example):
    return {
        "instruction": "Explain the medical concept step by step.",
        "input": example["instruction"],
        "output": example["output"]
    }


def token_length(sample):
    text = f"{sample['instruction']} {sample['input']} {sample['output']}"
    return len(text.split())


def save_jsonl(samples, path):
    with open(path, "w") as f:
        for s in samples:
            f.write(json.dumps({
                "instruction": s["instruction"],
                "input": s["input"],
                "output": s["output"]
            }) + "\n")


def main():
    dataset = load_from_disk(DATASET_PATH)["train"]

    qa_data = dataset.select(range(0, 500))
    reasoning_data = dataset.select(range(500, 1000)).map(make_reasoning_sample)
    extraction_data = dataset.select(range(1000, 1500)).map(make_extraction_sample)

    ## Adding commnets for my understanding :- Below is the final length of data
    final_data = concatenate_datasets([qa_data, reasoning_data, extraction_data]) 

    lengths = [token_length(s) for s in final_data]
    ##95 % values are smaller than this max_lenthj
    max_len = np.percentile(lengths, 95)

    cleaned = [
        s for s, l in zip(final_data, lengths) if l <= max_len
    ]

    np.random.seed(SEED)
    ## shuffling so that models see diverse instruction early : 
    np.random.shuffle(cleaned)
    ## from where splitting start : in my case total : Total samples : 1,426 * 0.9 => 1283 
    split_idx = int(len(cleaned) * 0.9)
    
    train_samples = cleaned[:split_idx]
    val_samples = cleaned[split_idx:]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_jsonl(train_samples, os.path.join(OUTPUT_DIR, "train.jsonl"))
    save_jsonl(val_samples, os.path.join(OUTPUT_DIR, "val.jsonl"))

    print(f"Train samples: {len(train_samples)}")
    print(f"Validation samples: {len(val_samples)}")


if __name__ == "__main__":
    main()

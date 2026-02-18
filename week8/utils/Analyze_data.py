import json
import os
from collections import Counter
import matplotlib.pyplot as plt


DATA_PATH = "data/train.jsonl"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def classify_task(instruction):
    inst = instruction.lower()
    if "extract" in inst:
        return "extraction"
    if "explain" in inst or "step by step" in inst:
        return "reasoning"
    return "qa"


def token_length(sample):
    text = f"{sample['instruction']} {sample['input']} {sample['output']}"
    return len(text.split())


def load_data():
    samples = []
    with open(DATA_PATH) as f:
        for line in f:
            samples.append(json.loads(line))
    return samples


def plot_token_distribution(samples):
    lengths = [token_length(s) for s in samples]
    plt.hist(lengths, bins=40)
    plt.xlabel("Token Length")
    plt.ylabel("Count")
    plt.title("Token Length Distribution")
    plt.savefig(os.path.join(OUTPUT_DIR, "token_length_distribution.png"))
    plt.close()


def plot_task_distribution(samples):
    tasks = [classify_task(s["instruction"]) for s in samples]
    counts = Counter(tasks)

    plt.bar(counts.keys(), counts.values())
    plt.xlabel("Task Type")
    plt.ylabel("Count")
    plt.title("Instruction Type Distribution")
    plt.savefig(os.path.join(OUTPUT_DIR, "task_type_distribution.png"))
    plt.close()


def main():
    samples = load_data()
    plot_token_distribution(samples)
    plot_task_distribution(samples)
    print("Plots saved in outputs/")


if __name__ == "__main__":
    main()

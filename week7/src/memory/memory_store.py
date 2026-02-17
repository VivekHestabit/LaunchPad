import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

LOG_FILE = Path("CHAT-LOGS.json")
LOG_FILE.touch(exist_ok=True)


class MemoryStore:
    def __init__(self, max_messages: int = 5):
        self.max_messages = max_messages
        self.memory = self._load()

    def _load(self) -> List[Dict]:
        if LOG_FILE.stat().st_size == 0:
            return []
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def add_message(self, question: str, answer: str):
        entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }

        self.memory.append(entry)
        self.memory = self.memory[-self.max_messages :]
        self._save()

    def get_memory(self) -> List[Dict]:
        return self.memory

    def get_prompt_context(self) -> str:
        if not self.memory:
            return ""

        lines = []
        for m in self.memory:
            lines.append(f"User: {m['question']}")
            lines.append(f"Assistant: {m['answer']}")

        return "\n".join(lines)

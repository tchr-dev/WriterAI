from pathlib import Path
import json
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_interaction(prompt: str, response: str, meta: dict = None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response,
        "meta": meta or {}
    }
    filename = datetime.utcnow().strftime("%Y-%m-%d") + ".jsonl"
    filepath = os.path.join(LOG_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_logs(path: str = "logs/2025-04-10.jsonl", limit: int = 20) -> list[dict]:
    entries = []
    p = Path(path)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries[-limit:]

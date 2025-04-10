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


def list_log_files(log_dir: str = "logs") -> list[str]:
    return sorted([str(p.name) for p in Path(log_dir).glob("*.jsonl")])


def load_logs_from_file(filename: str, log_dir: str = "logs", limit: int = 50) -> list[dict]:
    path = Path(log_dir) / filename
    entries = []

    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return entries[-limit:]

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

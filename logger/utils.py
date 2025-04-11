# logger/utils.py
import logging
import json
from datetime import datetime
from pathlib import Path

# Настройка логирования


def setup_logging(log_file="logs/interactions.log"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file, encoding='utf-8')]
    )

# Функция логирования взаимодействий


def log_interaction(user_input, llm_output, metadata=None):
    metadata = metadata or {}
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "llm_output": llm_output,
        "metadata": metadata,
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))

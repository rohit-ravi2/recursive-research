# tools/logger.py
import os
import json
from config import HISTORY_PATH

def log_project(state):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(state) + "\n")
    print("📚 Project logged to history.jsonl ✅")

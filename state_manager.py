# state_manager.py

import os
import json
import shutil
import logging
import git
import sys
from config import STATE_FILE, PROJECTS_PATH, HISTORY_PATH

# 🔧 Log to terminal instead of file
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_state():
    if os.path.exists(STATE_FILE):
        logging.info("📥 Loading previous state...")
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.warning(f"⚠️ Corrupted state.json: {e}")
            backup_path = f"{STATE_FILE}.corrupted"
            shutil.move(STATE_FILE, backup_path)
            logging.info(f"📦 Backed up corrupted state to: {backup_path}")
    
    logging.info("🆕 Starting with fresh state...")
    return {
        "iteration": 0,
        "idea": "",
        "status": "research",
        "log": [],
        "failures": 0,
        "papers": [],
        "dataset": {},
        "plan": "",
        "score": {"novelty": 0, "feasibility": 0, "impact": 0, "total": 0}
    }

def sanitize(obj):
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)

def deep_sanitize(state):
    visited = set()

    def _sanitize(obj):
        oid = id(obj)
        if oid in visited:
            return "<CircularRef>"
        visited.add(oid)
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_sanitize(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(_sanitize(i) for i in obj)
        else:
            return sanitize(obj)
    
    return _sanitize(state)

def save_state(state):
    sanitized = deep_sanitize(state)
    with open(STATE_FILE, "w") as f:
        json.dump(sanitized, f, indent=2)
    logging.info("✅ State saved.")

def archive_project(state, project_path):
    logging.info(f"📦 Archiving project: {state['idea']}")
    if state.get("status") != "complete":
        logging.info("⚠️ Skipping archive — status not 'complete'")
        return

    os.makedirs(project_path, exist_ok=True)
    with open(os.path.join(project_path, "state.json"), "w") as f:
        json.dump(deep_sanitize(state), f, indent=2)

    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps({
            "iteration": state["iteration"],
            "idea": state["idea"],
            "status": state["status"],
            "score": state.get("score", {}),
            "dataset": state.get("dataset", {}).get("name", ""),
            "papers": state.get("papers", []),
            "notebook_path": f"{project_path}/research_notebook.ipynb"
        }) + "\n")

    try:
        repo = git.Repo(".")
        repo.git.add(all=True)
        repo.git.commit(m=f"Add project: {state['idea']}")
        repo.git.push()
        logging.info("✅ Project committed to Git.")
    except Exception as e:
        logging.error(f"❌ Git commit failed: {e}")

    logging.info(f"📂 Archived project at: {project_path}")

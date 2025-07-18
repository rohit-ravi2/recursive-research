# tools/readme_generator.py
import os
import json
from config import HISTORY_PATH, README_PATH
import logging

def load_projects():
    if not os.path.exists(HISTORY_PATH):
        logging.info("No history.jsonl file found.")
        return []
    with open(HISTORY_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]

def write_readme_entry(state):
    projects = load_projects()
    projects.append({
        "idea": state["idea"],
        "status": state["status"],
        "score": state.get("score", {}).get("total", 0),
        "notebook_path": f"projects/{state['iteration']}_{state['idea'].replace(' ', '_')[:50]}/research_notebook.ipynb"
    })

    with open(README_PATH, "w") as f:
        f.write("# 🧠 Recursive Research Factory\n\n")
        f.write("| Topic | Score | Status | Notebook |\n")
        f.write("|-------|-------|--------|----------|\n")
        for p in projects[::-1]:
            nb = p.get("notebook_path", "-")
            score = p.get("score", "-")
            f.write(f"| {p['idea'][:40]}{'...' if len(p['idea']) > 40 else ''} | {score} | {p['status']} | [{os.path.basename(nb)}]({nb}) |\n")
    
    logging.info("Updated README with project entry.")
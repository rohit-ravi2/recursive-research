# tools/cleanup.py
import os
import shutil
from config import PROJECTS_PATH
import logging

def run_cleanup(score_threshold=4.0):
    count = 0
    for name in os.listdir(PROJECTS_PATH):
        path = os.path.join(PROJECTS_PATH, name)
        if os.path.isdir(path):
            try:
                readme_path = os.path.join(path, "README.md")
                if not os.path.exists(readme_path):
                    continue
                with open(readme_path) as f:
                    content = f.read()
                score_line = [line for line in content.splitlines() if "Score" in line]
                if score_line:
                    score = float(score_line[0].split(":")[-1].strip())
                    if score < score_threshold:
                        shutil.rmtree(path)
                        logging.info(f"Removed low-scoring project: {path}")
                        count += 1
            except Exception as e:
                logging.error(f"Cleanup failed for {path}: {e}")
    logging.info(f"Cleanup complete — {count} projects removed.")
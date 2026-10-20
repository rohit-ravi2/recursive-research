# config.py
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

# Project-wide paths
BASE_DIR = Path(__file__).parent
PROJECTS_PATH = BASE_DIR / "projects"
DATA_PATH = BASE_DIR / "data"
CACHE_PATH = DATA_PATH / "cache"
PAPERS_PATH = DATA_PATH / "papers"
DATASETS_PATH = DATA_PATH / "datasets"
LOGS_PATH = BASE_DIR / "logs"
HISTORY_PATH = LOGS_PATH / "history.jsonl"
STATE_FILE = BASE_DIR / "state.json"
VECTOR_STORE_PATH = BASE_DIR / "vectorstore" / "faiss_projects"
# Auto-generated index of completed projects (README.md is hand-written).
README_PATH = BASE_DIR / "PROJECTS_INDEX.md"

# Configuration
VECTOR_EMBED_MODEL = "all-MiniLM-L6-v2"
MAX_ITER = 3
HUMAN_REVIEW = True
NOVELTY_THRESH = 0.8
SCORE_THRESH = 7.0

# test_save_state.py
import json
state = {
    "idea": "Structure prediction using diffusion transformers",
    "score": {"novelty": 8, "feasibility": 8, "impact": 7, "total": 7.6},
    "plan": "some plan text",
    "dataset": {"name": "N/A"},
    "papers": ["Test paper A", "Test paper B"],
    "notebook_path": "projects/foo/notebook.ipynb"
}

with open("projects/test_state.json", "w") as f:
    json.dump(state, f, indent=2)

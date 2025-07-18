# test_notebook_build.py
from tools.notebook_builder import build_notebook
state = {
    "idea": "test idea",
    "plan": "This is a test plan.",
    "papers": ["Test Paper (http://example.com)"],
    "dataset": {"name": "dummy_dataset"}
}
build_notebook(state, "projects/test-notebook")

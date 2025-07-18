# tools/notebook_builder.py
import nbformat as nbf
from pathlib import Path
import datetime
import logging
from config import PROJECTS_PATH
import os

def build_notebook(state, project_path):
    logging.info(f"🧱 Building notebook for: {state['idea']}")
    
    notebook = nbf.v4.new_notebook()

    logging.info("✅ Assembling notebook cells...")

    # Safely render paper references
    papers = state.get("papers", [])
    paper_md = "\n".join(
        f"- {p}" if "http" not in p else f"- [{p.split(' (http')[0]}]({p.split(' (http')[1][:-1]})"
        for p in papers
    ) or "No papers found."

    cells = [
        nbf.v4.new_markdown_cell(f"# 🚀 Research Project: {state['idea']}"),
        nbf.v4.new_markdown_cell(f"Generated on: {datetime.datetime.now().isoformat()}"),
        nbf.v4.new_code_cell("# 📌 Set up environment\n!pip install -U torch transformers datasets"),
        nbf.v4.new_markdown_cell("## 🧠 Project Plan\n" + state.get("plan", "N/A")),
        nbf.v4.new_markdown_cell(f"## 📦 Dataset\n- **Dataset**: {state.get('dataset', {}).get('name', 'N/A')}"),
        nbf.v4.new_markdown_cell("## 📄 Key Papers\n" + paper_md)
    ]

    # Domain-specific starter code
    if "protein" in state["idea"].lower() or "rna" in state["idea"].lower():
        cells.append(nbf.v4.new_code_cell(
            f"""# 🧪 Model and Training
from datasets import load_dataset
import torch
from transformers import AutoModel

data = load_dataset('{state.get('dataset', {}).get('name', 'N/A')}')
model = AutoModel.from_pretrained('facebook/esm2_t33_650M_UR50D')
# Example training loop
for epoch in range(5):
    # Add training logic based on: {state.get('plan', '')}
"""
        ))
    else:
        cells.append(nbf.v4.new_code_cell(
            f"""# 🧪 Start coding
from datasets import load_dataset
data = load_dataset('{state.get('dataset', {}).get('name', 'N/A')}')
# Add model and training logic based on: {state.get('plan', '')}
"""
        ))

    notebook["cells"] = cells
    notebook_path = os.path.join(project_path, "research_notebook.ipynb")
    Path(project_path).mkdir(parents=True, exist_ok=True)
    
    logging.info("💾 Writing notebook file...")
    with open(notebook_path, "w") as f:
        nbf.write(notebook, f)

    logging.info(f"✅ Notebook saved at: {notebook_path}")
    return notebook_path

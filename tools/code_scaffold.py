# tools/code_scaffold.py
import os
from config import PROJECTS_PATH

def scaffold_notebook(project_name, dataset):
    slug = project_name.lower().replace(" ", "-")
    path = os.path.join(PROJECTS_PATH, slug)
    os.makedirs(path, exist_ok=True)

    notebook_path = os.path.join(path, "notebook.ipynb")

    content = f"""\
{{
 "cells": [
  {{
   "cell_type": "markdown",
   "metadata": {{}},
   "source": [
    "# Notebook: {project_name}"
   ]
  }},
  {{
   "cell_type": "code",
   "execution_count": null,
   "metadata": {{}},
   "outputs": [],
   "source": [
    "from datasets import load_dataset\\n",
    "data = load_dataset('{dataset.get('name')}')\\n"
   ]
  }}
 ],
 "metadata": {{}},
 "nbformat": 4,
 "nbformat_minor": 2
}}"""

    with open(notebook_path, "w") as f:
        f.write(content)

    return notebook_path

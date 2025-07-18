# agents/output_agent.py
import os
import logging
from config import PROJECTS_PATH, HUMAN_REVIEW
from tools.readme_generator import write_readme_entry
from tools.notebook_builder import build_notebook  # ✅ Make sure this import is present

class OutputAgent:
    def run(self, state):
        print(f"[DEBUG] 📝 OutputAgent running for: {state['idea']}")
        logging.info(f"Generating outputs for: {state['idea']}")
        try:
            idea = state["idea"]
            slug = idea.lower().replace(" ", "-")
            path = os.path.join(PROJECTS_PATH, slug)
            os.makedirs(path, exist_ok=True)

            # ✅ Write README.md
            with open(os.path.join(path, "README.md"), "w") as f:
                f.write(f"# {idea}\n\n")
                f.write(f"## Score\n{state['score']['total']}\n\n")
                f.write(f"## Plan\n{state['plan']}\n\n")
                f.write(f"## Dataset\n{state['dataset'].get('name', 'N/A')}\n\n")
                f.write("## Papers\n" + "\n".join(f"- {p}" for p in state["papers"]))

            # ✅ Write report.md
            with open(os.path.join(path, "report.md"), "w") as f:
                f.write(f"# Research Report: {idea}\n\n")
                f.write("## Abstract\n(TBD)\n\n")
                f.write("## Background\n")
                f.write("Inspired by:\n" + "\n".join(f"- {p}" for p in state["papers"]))
                f.write(f"\n\n## Method\n{state['plan']}\n\n")
                f.write("## Results\n(Placeholder)\n")

            # ✅ Build notebook
            notebook_path = build_notebook(state, path)
            state["notebook_path"] = notebook_path

            # ✅ Write to main project README
            write_readme_entry(state)

            logging.info(f"Generated all outputs for: {idea}")
            state["status"] = "review" if HUMAN_REVIEW else "complete"
            return state

        except Exception as e:
            logging.error(f"Output generation failed: {e}")
            state["status"] = "stop"
            return state

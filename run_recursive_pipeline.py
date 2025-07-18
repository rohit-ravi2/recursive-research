# run_recursive_pipeline.py

import json
import logging
import sys
from pathlib import Path

from tools.arxiv_search import search_arxiv
from tools.hf_datasets import find_dataset
from tools.notebook_builder import build_notebook
from tools.score_idea import score_idea
from tools.human_review import human_review

from agents.research_agent import ResearchAgent
from agents.execution_agent import ExecutionAgent
from agents.output_agent import OutputAgent
from agents.recursion_manager import RecursionManager

from state_manager import load_state, save_state, archive_project
from config import MAX_ITER, HUMAN_REVIEW

# 🔧 Log to terminal
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline(seed_topic=None):
    logging.info("🚀 Starting recursive research pipeline...")
    state = load_state()

    if seed_topic and state["iteration"] == 0:
        logging.info(f"🌱 Seeding pipeline with topic: {seed_topic}")
        state["idea"] = seed_topic
        state["status"] = "research"

    while state["iteration"] < MAX_ITER and state["status"] not in ["complete", "stop"]:
        logging.info(f"🔁 Iteration {state['iteration']} | Status: {state['status']} | Idea: {state['idea']}")
        try:
            if state["status"] == "research":
                logging.info("📚 ResearchAgent: Fetching papers and datasets...")
                research_agent = ResearchAgent()
                state["papers"], state["dataset"] = research_agent.run(state["idea"])
                logging.info(f"📚 Found {len(state['papers'])} papers and dataset: {state['dataset'].get('name', 'None')}")
                state["status"] = "execute"

            elif state["status"] == "execute":
                logging.info("🧠 ExecutionAgent: Generating research plan...")
                execution_agent = ExecutionAgent()
                state["plan"] = execution_agent.run(state)
                logging.info(f"🧠 Plan generated:\n{state['plan'][:200]}...")
                state["status"] = "score"

            elif state["status"] == "score":
                logging.info("📊 Scoring idea with LLM...")
                state["score"] = score_idea(state)
                logging.info(f"📊 Score: {state['score']}")
                state["status"] = "recursive"

            elif state["status"] == "recursive":
                logging.info("🔁 RecursionManager: Evaluating next steps...")
                recursion_manager = RecursionManager()
                state = recursion_manager.run(state)
                logging.info(f"🔁 Recursion status: {state['status']}")

            elif state["status"] == "review" and HUMAN_REVIEW:
                logging.info("🧑‍🔬 Human review phase started...")
                state = human_review(state)

            save_state(state)

        except Exception as e:
            logging.error(f"❌ Pipeline error at {state['status']}: {e}")
            state["failures"] = state.get("failures", 0) + 1
            save_state(state)

    if state["status"] == "complete":
        logging.info("✅ Finalizing output...")
        output_agent = OutputAgent()
        state = output_agent.run(state)

        project_slug = state['idea'].replace(' ', '-').lower()
        project_path = f"projects/{state['iteration']}_{project_slug[:50]}"
        notebook_path = build_notebook(state, project_path)
        state["notebook_path"] = notebook_path

        archive_project(state, project_path)

    logging.info("🏁 Pipeline finished.")
    logging.info(json.dumps(state, indent=2))


if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(seed)

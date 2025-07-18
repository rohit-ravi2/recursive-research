# tools/score_idea.py
import json
import logging
from pathlib import Path
from tools.llm_chain import llm_chain

def score_idea(state):
    logging.info("📊 Scoring idea with LLM...")

    try:
        prompt_path = Path("prompts/score_prompt.txt")
        prompt = prompt_path.read_text().format(idea=state["idea"])

        response = llm_chain.invoke(prompt)

        # ✅ Extract the actual string content
        if hasattr(response, "content"):
            response_text = response.content
        else:
            raise TypeError(f"Expected AIMessage, got: {type(response)}")

        logging.debug(f"[RAW LLM OUTPUT]\n{response_text}")

        # Grab only the JSON object (skip explanation if present)
        first_line = response_text.strip().split("\n")[0]
        parsed = json.loads(first_line)

        if not all(k in parsed for k in ["novelty", "feasibility", "impact", "total"]):
            raise ValueError("Missing keys in parsed score.")

        logging.info(f"📊 Score parsed successfully: {parsed}")
        return parsed

    except Exception as e:
        logging.error(f"❌ Pipeline error at score: {e}")
        logging.error(f"Raw LLM output:\n{response}")
        return {
            "novelty": 0,
            "feasibility": 0,
            "impact": 0,
            "total": 0.0
        }

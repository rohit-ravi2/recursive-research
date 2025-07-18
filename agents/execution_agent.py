# agents/execution_agent.py
from tools.llm import invoke_llm
from pathlib import Path
import logging

class ExecutionAgent:
    def run(self, state):
        logging.info(f"🧠 Generating plan for idea: {state['idea']}")
        try:
            if not isinstance(state, dict):
                raise TypeError(f"Expected state to be dict, got {type(state)}")
            idea = state.get("idea", "")
            if not idea:
                raise ValueError("No idea provided in state.")

            prompt_path = Path("prompts/execution_prompt.txt")
            prompt = prompt_path.read_text().format(idea=idea)
            logging.info("📝 Prompt for LLM prepared.")

            response = invoke_llm(prompt)
            if not isinstance(response, str):
                raise TypeError(f"Expected string response from LLM, got {type(response)}")

            logging.info("✅ Plan generated successfully.")
            return response.strip()
        except Exception as e:
            logging.error(f"❌ ExecutionAgent failed: {e}")
            return ""

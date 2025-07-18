import logging

class RecursionManager:
    def run(self, state):
        logging.info(f"Running RecursionManager for: {state['idea']}")
        try:
            score = state.get("score", {})
            if not isinstance(score, dict):
                raise TypeError(f"Expected score to be a dict, got: {type(score)} — value: {score}")

            total = score.get("total", 0)
            if total >= 7:
                logging.info("🎯 Score high — finalizing project.")
                state["status"] = "complete"
            elif state["iteration"] >= 2 or score.get("novelty", 0) < 5:
                logging.info("💤 Low novelty or too many iterations — stopping project.")
                state["status"] = "stop"
            else:
                logging.info("🔁 Recursing with updated idea...")
                state["idea"] += " (refined)"
                state["iteration"] += 1
                state["status"] = "research"
        except Exception as e:
            logging.error(f"RecursionManager failed: {e}")
            logging.error(f"🔍 Debug — state['score']: {state.get('score')}")
            state["status"] = "stop"  # Avoid infinite loop on failure
        return state

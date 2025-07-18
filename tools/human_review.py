# tools/human_review.py
import logging

def human_review(state):
    logging.info(f"Human review for: {state['idea']}")
    print(f"\n🧠 Human Review Checkpoint\nIdea: {state['idea']}\nScore: {state.get('score', {}).get('total', 0.0)}")
    print(f"Plan:\n{state.get('plan', '')[:1000]}\n")

    while True:
        choice = input("💬 Approve (a), Refine (r), Stop (s)? ").strip().lower()
        if choice in ["a", "r", "s"]:
            state["status"] = {"a": "complete", "r": "research", "s": "stop"}[choice]
            logging.info(f"Human review choice: {choice}")
            return state
        print("Invalid input. Choose 'a', 'r', or 's'.")
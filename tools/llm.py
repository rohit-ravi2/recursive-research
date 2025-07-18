# tools/llm.py
import requests
import hashlib
import pickle
import os
from config import CACHE_PATH
import logging

def invoke_llm(prompt: str, temperature: float = 0.7, model: str = "mistral") -> str:
    try:
        os.makedirs(CACHE_PATH, exist_ok=True)
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        cache_file = os.path.join(CACHE_PATH, f"{cache_key}.pkl")

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                return pickle.load(f)

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=20
        )
        res.raise_for_status()
        response = res.json().get("response", "").strip()

        with open(cache_file, "wb") as f:
            pickle.dump(response, f)
        
        return response
    except Exception as e:
        logging.error(f"Failed to invoke LLM: {e}")
        return ""
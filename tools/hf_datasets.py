# tools/hf_datasets.py
from huggingface_hub import list_datasets
import json
import os
from retry import retry
from config import DATASETS_PATH
import logging

@retry(tries=3, delay=2, backoff=2)
def find_dataset(topic):
    try:
        cache_file = os.path.join(DATASETS_PATH, f"{topic.replace(' ', '_')}.json")
        os.makedirs(DATASETS_PATH, exist_ok=True)

        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                logging.info(f"Loaded cached dataset for: {topic}")
                return json.load(f)

        datasets = list(list_datasets(search=topic, limit=1))
        dataset = {"name": datasets[0].id} if datasets and hasattr(datasets[0], 'id') else {"name": "No dataset found"}
        
        with open(cache_file, "w") as f:
            json.dump(dataset, f)
        
        logging.info(f"Dataset: {dataset.get('name', 'None')}")
        return dataset
    except Exception as e:
        logging.error(f"HF search failed: {e}")
        return {"name": "No dataset found"}
# tools/arxiv_search.py
import arxiv
import json
import os
from retry import retry
from config import PAPERS_PATH
import logging

@retry(tries=3, delay=2, backoff=2)
def search_arxiv(query, max_results=5):
    try:
        cache_file = os.path.join(PAPERS_PATH, f"{query.replace(' ', '_')}.json")
        os.makedirs(PAPERS_PATH, exist_ok=True)

        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                logging.info(f"Loaded cached papers for: {query}")
                return json.load(f)

        results = arxiv.Search(query=query, max_results=max_results)
        papers = [f"{r.title} ({r.entry_id})" for r in results.results()]
        with open(cache_file, "w") as f:
            json.dump(papers, f)
        
        logging.info(f"Found {len(papers)} papers for: {query}")
        return papers
    except Exception as e:
        logging.error(f"ArXiv search failed: {e}")
        return []
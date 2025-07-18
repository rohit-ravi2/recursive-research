# tests/test_tools.py
import pytest
from tools.score_idea import score_idea
from tools.arxiv_search import search_arxiv
from tools.hf_datasets import find_dataset

def test_score_idea():
    state = {"idea": "test idea"}
    scores = score_idea(state)
    assert isinstance(scores, dict)
    assert "total" in scores

def test_arxiv_search():
    papers = search_arxiv("test", max_results=1)
    assert isinstance(papers, list)

def test_hf_datasets():
    dataset = find_dataset("test")
    assert isinstance(dataset, dict)
    assert "name" in dataset
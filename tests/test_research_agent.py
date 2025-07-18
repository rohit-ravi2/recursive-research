# tests/test_research_agent.py
import pytest
from agents.research_agent import ResearchAgent

def test_research_agent():
    agent = ResearchAgent()
    papers, dataset = agent.run("diffusion models")
    assert isinstance(papers, list)
    assert isinstance(dataset, dict)
    assert "name" in dataset
# tests/test_execution_agent.py
import pytest
from agents.execution_agent import ExecutionAgent

def test_execution_agent():
    agent = ExecutionAgent()
    state = {"idea": "diffusion models for RNA folding"}
    plan = agent.run(state)
    assert isinstance(plan, str)
    assert len(plan) > 0
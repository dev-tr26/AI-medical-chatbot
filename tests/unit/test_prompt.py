# tests/unit/test_prompt.py
from src.prompt import system_prompt

def test_system_prompt_contains_context():
    assert "{context}" in system_prompt
    assert "concise" in system_prompt

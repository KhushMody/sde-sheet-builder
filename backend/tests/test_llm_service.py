import pytest
from app.services.llm_service import call_llm

def test_call_llm():
    """Test LLM response parsing."""
    system_message = "Test system prompt"
    user_message = "Solve Two Sum"
    
    response = call_llm(system_message, user_message)
    
    assert response is not None
    assert isinstance(response, str)  # Assuming response is a string

# /app/tests/test_api.py
import pytest
import json

def test_analyze_question(client):
    """Test the /api/analyze endpoint with test data."""
    response = client.post("/api/analyze", json={"question": "Suggest medium difficulty Google questions about arrays and give 1 question"})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert "data" in data
    assert len(data["data"]) > 0  # Ensure at least one question is returned
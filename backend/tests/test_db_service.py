# /app/tests/test_db_service.py
import pytest
from app.services.db_service import get_data

def test_get_data(app):
    """Test fetching data from database service within Flask app context."""
    with app.app_context():
        company_name = "google"
        data = get_data(company_name)  # Runs inside the app context
        assert data is not None
        assert len(data) > 0  # Ensure test data exists
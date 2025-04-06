# /app/tests/conftest.py
import pytest
from app.services.db_service import get_data
from app.app import create_app, db
from app.models import Question

@pytest.fixture
def app():
    print("🚀 Starting app fixture")

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    }

    app = create_app(test_config=test_config)

    with app.app_context():
        print("📦 In app context, creating tables")
        db.create_all()
        try:
            print("📝 Inserting test data")
            test_questions = [
                Question(
                    company="google",
                    question="array based two sum",
                    acceptance="50%",
                    difficulty="Medium",
                    question_link="https://leetcode.com/problems/two-sum/description/?envType=problem-list-v2&envId=array"
                )
            ]
            db.session.bulk_save_objects(test_questions)
            db.session.commit()
            yield app
        finally:
            print("🧹 Dropping tables")
            db.drop_all()


@pytest.fixture
def client(app):
    """Fixture to create a test client."""
    return app.test_client()
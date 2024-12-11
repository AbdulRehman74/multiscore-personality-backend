from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_questions():
    response = client.get("/api/v1/questions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Assuming at least one question
    assert "id" in data[0]
    assert "text" in data[0]
    assert "category" in data[0]

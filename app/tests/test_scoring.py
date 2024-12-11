from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_score_responses():
    response = client.post(
        "/api/v1/score",
        json={
            "responses": [
                {"question_id": 1, "answer": "Agree"},
                {"question_id": 2, "answer": "Neutral"},
                {"question_id": 3, "answer": "Disagree"}
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert "dominant_preferences" in data

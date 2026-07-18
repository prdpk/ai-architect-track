from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_greeting():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, RAG API",
    }


def test_ask_rejects_missing_question():
    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_ask_returns_answer(monkeypatch):
    monkeypatch.setattr(
        "app.main.ask_rag",
        lambda question: "Mocked answer.",
    )

    response = client.post(
        "/ask",
        json={
            "question": "Is theft covered?",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Mocked answer.",
    }
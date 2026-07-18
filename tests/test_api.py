from fastapi.testclient import TestClient
from app.backends.base import RAGBackend
from app.rag import get_backend


from app.main import app

client = TestClient(app)

class FakeBackend(RAGBackend):
    def answer(self, question: str) -> str:
        return "Mocked answer."


app.dependency_overrides[get_backend] = lambda: FakeBackend()


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

def test_ask_returns_answer():
    response = client.post("/ask", json={"question": "Is theft covered?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked answer."}

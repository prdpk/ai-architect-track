from fastapi import Depends, FastAPI
from app.backends.base import RAGBackend
from app.rag import get_backend
from app.schemas import AskRequest, AskResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Hello, RAG API"
    }

@app.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    backend: RAGBackend = Depends(get_backend),
) -> AskResponse:
    result = backend.answer(request.question)
    return AskResponse(answer=result)
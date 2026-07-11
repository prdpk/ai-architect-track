from fastapi import FastAPI

from app.rag import ask_rag
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
) -> AskResponse:
    result = ask_rag(request.question)

    return AskResponse(
        answer=result,
    )
from fastapi import FastAPI
from app.rag import answer
from app.schemas import AskRequest, AskResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, RAG API"}

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    result = answer(request.question)

    return AskResponse(
        answer=result,
    )
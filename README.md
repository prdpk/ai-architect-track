# AI Architect Track — Policy Q&A (RAG service)

## Overview

A small but production-shaped **Retrieval-Augmented Generation (RAG)** service. It
answers natural-language questions about a set of insurance policy documents and
returns answers **grounded in those documents** — if the answer isn't in the
policies, it says so instead of guessing.

The flow is the classic RAG loop:

1. **Retrieve** — embed the user's question and find the most relevant chunks of
   the policy documents from a vector store.
2. **Augment** — build a prompt that includes only those retrieved chunks as context.
3. **Generate** — ask Claude to answer *using only that context*.

The service is exposed over HTTP (FastAPI), with a JSON `/ask` API, auto-generated
API docs, and a minimal browser UI.

> All policy data in this repo is **synthetic**. There is no real policy, customer,
> or trading data anywhere in this project.

---

## Architecture

The design goal is that the *retrieval engine is an implementation detail* hidden
behind a stable API.

- **Stable JSON contract.** `POST /ask` takes `{"question": "..."}` and returns
  `{"answer": "..."}`. Every client — the browser UI, `curl`, Swagger, a future
  mobile app — speaks the same contract. The UI is a static page that calls this
  same API; it is not privileged.
- **Swappable backends (strategy pattern).** A `RAGBackend` interface (an abstract
  base class) has two interchangeable implementations selected by config:
  - `langchain` — LangChain pipeline (RecursiveCharacterTextSplitter →
    HuggingFace embeddings → in-memory Chroma → retriever → ChatAnthropic, wired
    as an LCEL chain).
  - `manual` — hand-rolled pipeline (SentenceTransformers embeddings → persistent
    ChromaDB → cosine retrieval → Anthropic SDK call).
  
  Both produce equivalent grounded answers for the same question. Swapping
  `RAG_BACKEND` changes the engine without touching the API, the schema, or the tests.
- **Dependency injection.** The `/ask` endpoint receives its backend via FastAPI's
  `Depends(get_backend)`. The real backend is built lazily and cached
  (`@lru_cache`) — built once, on the first real request, not at import. Tests
  override this dependency with a fake, so the real pipeline (model load,
  embedding) never runs during testing.
- **Grounding over trust.** The prompt instructs Claude to answer *only* from the
  retrieved context and to say "I don't have that information" otherwise. This is
  the anti-hallucination safety net — the model is not allowed to answer from its
  own prior knowledge.
- **Config, not code.** Secrets and tunable knobs (model, chunk size, top-k,
  backend choice, log level) live in configuration, not in source.

See [docs/design-note.md](docs/design-note.md) for the architecture decision record.

---

## Prerequisites

- Python 3.11 or later
- Git
- An Anthropic API key with available API credits

---

## Installation

Clone the repository:

```bash
git clone https://github.com/prdpk/ai-architect-track.git
cd ai-architect-track
```

Create and activate a virtual environment.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Configuration is loaded from a `.env` file in the project root (via Pydantic
`BaseSettings`). Create one — it is git-ignored and must never be committed:

```dotenv
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional (defaults shown)
LLM_MODEL=claude-haiku-4-5
MAX_TOKENS=200
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=300
CHUNK_OVERLAP=50
TOP_K=2
RAG_BACKEND=langchain        # or: manual
LOG_LEVEL=INFO               # DEBUG shows per-request retrieval + prompts
```

> **Precedence gotcha:** OS environment variables **override** `.env`. If you have
> `ANTHROPIC_API_KEY` exported in your shell, that value wins over the one in
> `.env` — so `unset ANTHROPIC_API_KEY` if you want `.env` to be the single source.

---

## Project Structure

```text
ai-architect-track/
├── app/                        # the deployable service
│   ├── main.py                 # FastAPI app: GET / (health), POST /ask, /static UI
│   ├── schemas.py              # Pydantic request/response models (free 422 validation)
│   ├── config.py               # Pydantic BaseSettings (.env) + logging setup
│   ├── rag.py                  # backend factory + DI provider (get_backend)
│   ├── backends/
│   │   ├── base.py             # RAGBackend interface (ABC)
│   │   ├── langchain_backend.py
│   │   └── manual_backend.py
│   └── static/
│       └── index.html          # minimal web UI (form → fetch('/ask'))
├── data/
│   └── policies/               # synthetic insurance policy documents
├── tests/
│   └── test_api.py             # pytest + TestClient (backend overridden via DI)
├── scripts/                    # earlier learning spikes (see below)
├── docs/
│   └── design-note.md          # architecture decision record
├── pytest.ini                  # bounds test discovery to tests/
├── requirements.txt
└── README.md
```

---

## Running the Service

Start the API (with auto-reload) from the project root:

```bash
fastapi dev app/main.py
```

Then:

- **Web UI:** open <http://127.0.0.1:8000/static/> and ask a question.
- **Interactive API docs:** <http://127.0.0.1:8000/docs>
- **Direct API call:**

  ```bash
  curl -X POST http://127.0.0.1:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "Is theft covered?"}'
  ```

  Example response:

  ```json
  {
    "answer": "Yes, theft is covered under this policy, but with specific conditions: ..."
  }
  ```

To run against the hand-rolled engine instead of the LangChain one, override the
backend for that process (this also demonstrates the config-driven swap):

```bash
RAG_BACKEND=manual fastapi dev app/main.py
```

> The first `/ask` after startup is slower (several seconds): the backend is built
> lazily on first use — models load and documents are embedded — then cached for
> the life of the process.

---

## Testing

```bash
pytest
```

The suite uses FastAPI's `TestClient` and overrides the backend dependency with a
fake, so tests are fast and require no API call. `pytest.ini` bounds discovery to
`tests/` so the `scripts/` experiments are not collected.

---

## Learning progression (`scripts/`)

This is a learning repository; `scripts/` holds the earlier spikes that led to the
service above, kept for history:

- `first_call.py`, `summarize.py`, `analyze_trades.py` — first Claude API calls and
  the numbers-from-code / words-from-LLM lesson (Phase 1).
- `rag_demo.py`, `rag_chunked.py`, `rag_chunked_overlap.py`, `rag_langchain.py` —
  RAG built up from a hand-rolled cosine search to a full LangChain pipeline (Phase 2).
- `eval_retrieval.py`, `eval_answers.py`, `test_reranker.py` — retrieval hit-rate,
  LLM-as-judge answerability, and reranking experiments (Phase 2).

These are experiments, not part of the deployed service.

---

## Limitations

- Uses **synthetic** policy data for demonstration only — no real policy, customer,
  or trading data.
- Requires a valid Anthropic API key; `/ask` makes a paid API call (a fraction of a
  cent per question on Claude Haiku).
- No authentication, rate limiting, or persistence of Q&A history — this is a
  learning/portfolio service, not a hardened production deployment.
- The `langchain` backend builds its vector store **in memory** and re-embeds on
  every process start; the `manual` backend persists embeddings to a local
  `chroma_db/` directory (embed-once).
- Answers are only as good as the retrieved context; retrieval quality is bounded
  by chunking and `TOP_K`.

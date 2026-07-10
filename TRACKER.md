# Tracker — single source of truth for progress

> Update at the end of every working session. Keep entries short. This is the
> state CT and chat-Claude drive from — if it isn't written here, it didn't happen.

## Now
- Phase: 3 — Script -> service: backend + APIs (STARTING). Phase 2 app-layer core
  done (RAG hand-rolled + framework + evals + reranking + LLM-as-judge).
- Next action: Phase 3 gate — HTTP/REST, what an API is, FastAPI, request
  lifecycle. Then wrap the RAG behind a real API endpoint (build pipeline once at
  startup, invoke per request — the shape the operator already derived). Later:
  a DB + ORM, config, testing, a simple web UI. Working CS literacy woven in here.

## Status
- Started on: 2026-06-22
- On pace? (yes / behind / ahead): yes
- Current blocker (if any): none

## Done log
(newest first — one line each: date — what shipped — verified yes/no)
- 2026-07-11 — Phase 2 evals part 2: measure->fix->re-measure loop. Fixed chunking
  (paragraph splits) → flood miss resolved, 60%->80% (diagnosis-first). Added
  cross-encoder reranking (fixed L6->L12 NaN-on-Apple-Silicon bug); learned rerank
  absolute scores are ALSO uncalibrated + reranker only reorders (no benefit on
  clean data — right-fit evidence to omit it). Built LLM-as-judge answerability
  (eval_answers.py): separate Claude call reads question+context → YES/NO. SOLVED
  the earthquake unanswerable case no threshold could. Learned "grade the grader":
  the waterlogged-basement fail was a bad golden label, not a system bug. — verified yes
- 2026-07-09 — Phase 2 evals: passed evals gate (one query ≠ representative; need
  a golden set with expected outputs; retrieval vs answer quality fail
  independently). Built scripts/eval_retrieval.py (hit rate over a golden set).
  Learned that a green eval can be too weak to fail → hardened with adversarial
  paraphrases + an unanswerable earthquake case: 100% → 60%, measuring the SAME
  chunking (flood smeared) + threshold-miscalibration (earthquake 0.52 > legit
  0.28) problems reasoned earlier. Meta-lesson: a good eval is one you can fail.
  Operator authored. — verified yes
- 2026-07-03 — Phase 2 orchestration framework: implemented overlap chunking
  (rag_chunked_overlap.py, sliding window) + reasoned chunk-size/overlap and
  derived recursive/structure-aware splitting; measured the size/specificity
  tradeoff (bigger chunk → higher distance 1.04 vs 0.70, richer answer). Rebuilt
  the whole RAG via LangChain (rag_langchain.py): RecursiveCharacterTextSplitter,
  HuggingFaceEmbeddings, Chroma, as_retriever, ChatAnthropic, ChatPromptTemplate,
  LCEL chain. Reasoned the transparency tradeoff (concise but hidden flow),
  eager-index vs lazy-chain, and query = only dynamic input → deployment shape.
  Operator authored + defended the mapping. — verified yes
- 2026-07-02 — Phase 2 RAG deepened: reasoned threshold role (cost filter, not
  correctness; scores uncalibrated — earthquake 0.43 bad > laptop 0.35 good),
  re-ranking, grounding-as-safety-net. Built chunking (split doc → chunks) and
  chunk-size/overlap reasoning. Wired Chroma vector DB (rag_chunked.py):
  bring-your-own sentence-transformers embeddings, PersistentClient, embed-once
  guard, distance-based retrieval (L2, lower=closer). Verified persistence across
  process restarts. chroma_db/ gitignored. Operator authored. — verified yes
- 2026-06-29 — PHASE 2 START: passed RAG/embeddings gate (retrieve→augment→
  generate; embeddings = meaning vectors; same-model query; semantic > keyword).
  Built minimal hand-rolled RAG (scripts/rag_demo.py): local sentence-transformers
  (all-MiniLM-L6-v2) embeds synthetic policy snippets, cosine-sim retrieval (util.
  cos_sim), top match → grounded Claude prompt. Verified: "broke in/took laptop"→
  theft snippet (semantic, 0 keyword overlap); "earthquake?"→"I don't have that"
  (anti-hallucination grounding). Insight: retrieval always returns a top match →
  need a score THRESHOLD. Operator authored. — verified yes
- 2026-06-29 — Wk4 SHIP: repo pushed to GitHub (github.com/prdpk/ai-architect-track,
  public, SSH). README.md (overview/prereqs/install/config/structure/run/output/
  limitations, incl. run-from-scripts import gotcha) + docs/design-note.md (ADR:
  numbers-from-code/words-from-LLM, 3 tradeoffs, 3 scale changes incl. caching).
  Operator authored both, passed gate (README purpose, what an ADR is + why).
  PHASE 1 COMPLETE. — verified yes
- 2026-06-29 — Wk3 build DONE (right-design): analyze_trades.py now imports
  load_trades/summarize_trades from summarize module, computes numbers in code
  (total_quantity=275 exact, no LLM math), LLM produces ONLY the prose summary,
  result assembled as dict. FileNotFoundError handled at call site (load_trades
  kept pure). Verified missing-file path (clean msg, no traceback). Done bar met:
  CSV-in→structured-out, env key, missing-file, functions/module. — verified yes
- 2026-06-29 — Wk3 functions/modules + structured output: refactored summarize.py
  into pure functions (load_trades/print_trades/summarize_trades, tuple return)
  + `if __name__=="__main__"` module guard; output unchanged (10/6/4/275).
  analyze_trades.py: prompt→JSON→json.loads→dict field access (structured output).
  BIG LESSON: LLM is not a calculator — model returned total_quantity=235 vs
  correct 275 (induced + caught a hallucination). Rule learned: numbers from
  code, words from LLM. Operator authored; explained single-responsibility,
  __name__, json.loads, math-vs-language split. — verified yes
- 2026-06-28 — Wk2 first LLM call: API billing set up ($5 spend cap), anthropic
  SDK pinned in requirements.txt, ANTHROPIC_API_KEY via env var. scripts/
  first_call.py (live Haiku call, parse content[0].text + usage) and
  summarize_trades.py (prompt = instruction + synthetic rows → summary).
  Operator authored; explained key=spendable-password, request/response shape,
  token cost math (~$0.0001/call), AuthenticationError on missing key,
  max_tokens truncation. NOTE: summarize_trades.py max_tokens bumped 100→400
  (was truncating). — verified yes
- 2026-06-28 — scripts/summarize.py: reads synthetic CSV via csv.DictReader,
  prints count/BUY-SELL/total-qty; try/except FileNotFoundError; __file__-anchored
  path (runs from any cwd). Operator authored; passed knowledge check (with vs
  try, int() type trap, .resolve(), silent-else failure mode) — verified yes
- 2026-06-22 — Python 3.13.2 confirmed; venv created (.venv), activated, `which
  python` verified inside venv; learned venv mechanism + auto `.venv/.gitignore` — verified yes
- 

## Open questions / to revisit
- 

## Decisions parked for later
- Geo + cert target (deferred — revisit at Phase 6)
- Spine project PINNED: financial/insurance Document & Data Intelligence platform
  on synthetic data (see PLAN.md "Spine project"). Grows across all phases.
- Cloud choice: AWS vs Azure (decide at Phase 4)
- AT PHASE 5 BOUNDARY: first build PHASE5.md = full system-design syllabus, so all
  architect concepts (incl. unknown-unknowns) get covered by structure. Heavy
  patterns covered via study + isolated spikes, not force-fit onto the spine.
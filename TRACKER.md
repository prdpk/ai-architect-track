# Tracker — single source of truth for progress

> Update at the end of every working session. Keep entries short. This is the
> state CT and chat-Claude drive from — if it isn't written here, it didn't happen.

## Now
- Phase: 1 — Foundations through a first real build (COMPLETE)
- Week: 4 — Ship + design note (DONE)
- Next action: PHASE 2 — RAG & the AI application layer (spine slice 1: RAG
  Q&A over synthetic policy docs). Gate concepts before any build: embeddings,
  vector DBs, chunking, retrieval, one orchestration framework. Source learning,
  then gate.

## Status
- Started on: 2026-06-22
- On pace? (yes / behind / ahead): yes
- Current blocker (if any): none

## Done log
(newest first — one line each: date — what shipped — verified yes/no)
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
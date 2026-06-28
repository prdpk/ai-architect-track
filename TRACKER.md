# Tracker — single source of truth for progress

> Update at the end of every working session. Keep entries short. This is the
> state CT and chat-Claude drive from — if it isn't written here, it didn't happen.

## Now
- Phase: 1 — Foundations through a first real build
- Week: 1 — Python unblocked
- Next action: Wk1 DONE. Next is Wk2 — first LLM call (gate: API keys/env vars,
  request→response, tokens & cost) before any code.

## Status
- Started on: 2026-06-22
- On pace? (yes / behind / ahead): yes
- Current blocker (if any): none

## Done log
(newest first — one line each: date — what shipped — verified yes/no)
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
- Phase 2 spine project (likely RAG over synthetic policy/log data — pin at Phase 2)
- Cloud choice: AWS vs Azure (decide at Phase 4)

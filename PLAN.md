# Learning Plan — Technical Architect, AI-fluent, owns end-to-end

## Target
Become a credible, hireable Technical Architect who is AI-fluent and can own a
project end-to-end (requirements → design → tech choices → guiding the build →
deployment → non-functionals). System design is the spine; AI is the layer;
financial-domain experience is the wedge. The proof is a portfolio of deployed,
explainable systems — not courses or certs.

## Finish line (definition of done for the whole journey)
Done = (1) at least one AI system deployed and publicly reachable, (2) two
written architecture case studies explaining the design and tradeoffs, and
(3) able to hold a system-design conversation and defend the decisions.
That is the result everything here is aimed at.

## How this plan runs (read with CLAUDE.md)
- LEARN BEFORE BUILD. Operator does the actual learning; CT verifies
  understanding before any build. See CLAUDE.md "learning gate".
- LEARNING RESOURCES. Per topic: 1-2 current, phase-aligned resources, curated
  minimal (never a playlist) - either chat-Claude pulls them via web search, or
  operator uses their own. Chat-Claude also tutors in-chat (explains, quizzes,
  debugs). The operator still does the learning; the gate verifies it.
- One phase at a time. Each phase ends in a VERIFIED, EXPLAINABLE outcome.
- Time budget: ~8 hrs/week, split learn/build. Learn share starts ~40% and
  trends to ~15–20% by later phases. Leftover learn time rolls into build.
- DSA is NOT front-loaded. Working CS literacy is woven into Phase 3 (real code)
  and Phase 5 (design tradeoffs). A LeetCode sprint is added later ONLY if a
  target role demands it.
- BUILD IN SLACK. Each phase includes catch-up buffer. Life will disrupt 8
  hrs/week; falling behind is expected and normal, NOT a reason to quit. Adjust
  the timeline, never abandon it.
- Durations are estimates, not contracts. Phases 4–6 are DIRECTIONAL and will be
  re-detailed nearer the time (cloud + AI tooling move too fast to hard-spec now).

## Pipeline order
Python → AI application layer (RAG/agents) → backend + APIs → cloud + deploy →
system design (spine) → consolidation + positioning.

---

## PHASE 1 — Foundations through a first real build  (~4 weeks)
Outcome: Python unblocked; first LLM-powered tool over SYNTHETIC data; on
GitHub; with a 1-page design note.

- Wk 1 — Python unblocked. Learn ~3.5h / Build ~4.5h.
  Learn: syntax, data types, functions, file reading, venv, pip, project layout.
  Build: script that reads a synthetic CSV and prints a basic summary (no AI).
  Done: venv works, script prints correct numbers, operator can explain each line.

- Wk 2 — First LLM call. Learn ~3h / Build ~5h.
  Learn: API keys/secrets (env vars), request→response, tokens & cost.
  Build: script that calls an LLM and summarizes 3 fake trade rows.
  Done: real API response; operator can explain a token and rough call cost.

- Wk 3 — Make it a real tool. Learn ~2.5h / Build ~5.5h.
  Learn: functions/modules, prompt structure, structured output.
  Build: CSV-in → structured-analysis-out tool; env-var key; handles missing file.
  Done: one command → readable structured analysis; code in functions.

- Wk 4 — Ship + design note. Learn ~1.5h / Build ~6.5h.
  Learn: README/repo conventions, what a design note / ADR is.
  Build: push to GitHub with clean README; write 1-page design note (decisions
  + 2–3 tradeoffs + "what I'd change at scale").
  Done: a stranger can run it from the README; the note explains WHY, not just what.

---

## PHASE 2 — RAG & the AI application layer  (~6–8 weeks, directional)
Learn: embeddings, vector DBs, chunking, retrieval, prompting patterns, tool/
function calling, one orchestration framework; applied AI literacy (context
windows, hallucination, evals).
Build: a RAG / analytics app over messy real-SHAPED data — use SANITIZED EA log
schemas + synthetic data as substrate (no real strategy logic, ever).
Outcome: working RAG app + design note on retrieval tradeoffs.

## PHASE 3 — Script → service: backend + APIs  (~6 weeks, directional)
Learn: HTTP/REST, FastAPI, request lifecycle, a database (SQL + an ORM), config,
testing basics. Working CS literacy (core data structures, big-O intuition) is
learned HERE, inside real code.
Build: the tool wrapped behind a real API + a simple web UI (leverage FE skill).
Outcome: a running service with API docs.

## PHASE 4 — Cloud + deployment  (~6 weeks, directional)
Learn: Docker, ONE cloud (AWS vs Azure — decide here), a deploy path, CI/CD,
secrets, basic observability/logging, cost.
Build: containerize and deploy the Phase 3 service; add a CI/CD pipeline + basic
monitoring.
Outcome: a publicly deployed, monitored AI app — the "production" proof.

## PHASE 5 — System design & architecture: the spine  (~6–8 weeks, directional)
Learn: architecture vocabulary (sync/async, queues, caching, statelessness,
consistency, scaling patterns), NFRs, security/governance (finance lens),
guardrails/evals, cost control, ADRs & diagrams. Design-relevant DSA resurfaces
here as complexity/data-modeling tradeoffs.
Build: re-architect one app for scale on paper + implement 1–2 upgrades.
Outcome: ADRs + architecture diagrams + a "scale this to X" design doc.

## PHASE 6 — Consolidation & positioning  (~4–6 weeks, directional)
Learn: solutioning/communication, architecture case-study writing; make the
deferred geo + cert decision here.
Build: package 2–3 projects as architecture case studies + positioning.
Outcome: a portfolio ready to apply or pitch.

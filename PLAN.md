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

## Career strategy (path to the role)
Target the CAPABILITY, not the title — the title follows the capability, not the
other way round. Preferred path: grow architecture scope INSIDE the current org
as capability develops (~Phase 3+). Ask for and own design decisions / a component
end-to-end once the system-design vocabulary is real — earn the vocabulary BEFORE
claiming the scope, not before. Convert learning into owned responsibility at
work; that real experience + built artifacts = architect-level credibility,
internal or external. Motivation on record: wants to own systems end-to-end, not
fix bugs for life — this is the fuel for the slow months.

## Spine project (the thing we grow across all phases)
A financial/insurance DOCUMENT & DATA INTELLIGENCE platform, built on SYNTHETIC
data only (IP-safe — no real Mahakal logic or data). It ingests synthetic policy
documents + synthetic structured records and provides: RAG-grounded Q&A over the
documents, natural-language analytics over the structured data, and a dashboard.
Chosen because its complexity is REAL (slow ingestion → genuine reason for async
queues; costly LLM calls → genuine reason for caching; financial data → genuine
reason for observability, audit, security). So building it right-fit exercises
most of the architect surface for honest reasons, not force-fit.
Phase 2 builds the first slice of this spine (RAG over the synthetic data).

## Two-track learning (how breadth gets covered without wrong instincts)
- SPINE = built RIGHT-FIT, the way an architect actually would. Uses patterns
  that truly fit; deliberately omits ones that don't — and can explain why.
  This is the portfolio + the proof of judgment.
- SPIKES = small, isolated, throwaway labs for heavy patterns that do NOT fit
  the spine (Kafka, Kubernetes, microservices, sharding). Goal: feel the pattern
  hands-on, then articulate its tradeoff. NOT bolted onto the spine.
- Rule: never force-fit a pattern onto the spine just to "use" it. Knowing when
  NOT to use something is the architect skill being graded.

## Coverage commitment (the unknown-unknowns guarantee)
- At the Phase 5 boundary, FIRST build PHASE5.md: a full system-design syllabus
  (the industry-standard checklist) so concepts get covered by structure, not by
  what the operator thinks to ask. Examples to include: caching/CDN, load
  balancing, message queues/Kafka, CAP theorem, indexing/sharding/replication,
  API gateways/rate limiting/idempotency, observability, failure design (retries,
  circuit breakers, SPOF), security/auth patterns, cost/capacity, monolith vs
  microservices, common patterns (CQRS, event-driven, saga).
- Honest calibration: "in depth" here = can DECIDE and DEFEND every concept +
  hands-on with the core (spine) + spiked breadth on the heavy ones. It does NOT
  mean production-specialist in every technology. Nobody is, and the role does
  not require it.

## How this plan runs (read with CLAUDE.md)
- LEARN BEFORE BUILD. Operator does the actual learning; CT verifies
  understanding before any build. See CLAUDE.md "learning gate".
- LEARNING RESOURCES. Per topic: 1-2 current, phase-aligned resources, curated
  minimal (never a playlist). CT can pull these itself via its WebSearch/WebFetch
  tools - keep it inline, in flow. Chat-Claude can also pull them for broader
  curation or a second opinion, or operator uses their own. Either way the
  operator does the learning; the gate verifies it.
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
Build: the FIRST SLICE of the spine (see "Spine project") — RAG-grounded Q&A
over SYNTHETIC policy documents. Synthetic data only; no real Mahakal logic or
data, ever. Keep the slice thin and shippable; later phases grow it.
Outcome: working RAG app (spine slice 1) + design note on retrieval tradeoffs.

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
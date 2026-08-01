# Phase 5 — System Design & Architecture Syllabus

> This file exists to prevent unknown-unknowns. Every topic an architect is
> expected to know is listed here by structure, not by what came to mind.
> Work through it in order; do not skip ahead. Each topic has a track:
> SPINE (built into the policy-QA app), SPIKE (isolated throwaway lab), or
> STUDY (concept + verbal defence, no code required).

## How Phase 5 runs

- Learn the concept -> explain it in your own words (gate) -> build or defend it.
- Every SPINE topic produces a real code change + an ADR in docs/.
- Every SPIKE produces a throwaway script + 1 paragraph: "when I'd use this
  and when I wouldn't."
- STUDY topics end in a verbal defence (quiz with CT).
- SEQUENCE: vocabulary-first. Block 1 before anything else, then proceed in order.
- Final deliverables: (1) a "scale this to 10x users" design doc for the spine
  app, and (2) the AI-analytics-SaaS design-on-paper case study (see end).

## Honest depth calibration (read once)
- SPINE = real hands-on depth on the app.
- SPIKE = touched, working, tradeoff-articulable — NOT production-specialist.
- STUDY = decide + defend, no build.
- "Learning it all for real" = the above, per track. It does NOT mean operating
  every technology in production like a specialist. Nobody clears that bar and
  the architect role does not require it. Depth accrues later, on real jobs.

---

## Block 1 — Foundations (no code yet, vocabulary first)

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 1.1 | Sync vs async — what changes at the call site, the server, the failure model | STUDY | Can explain with a concrete example (e.g. /ask today is sync — what breaks at scale) |
| 1.2 | Stateless vs stateful — why stateless services scale horizontally | STUDY | Can explain why our FastAPI app is stateless and what would make it stateful |
| 1.3 | Horizontal vs vertical scaling — tradeoffs, limits of each | STUDY | Can say when vertical stops working and what horizontal requires |
| 1.4 | CAP theorem — consistency, availability, partition tolerance; pick two | STUDY | Can place Chroma and a SQL DB on the CAP triangle and defend it |
| 1.5 | Latency vs throughput — why optimising one can hurt the other | STUDY | Can give a concrete example from our app |

---

## Block 2 — Data Layer

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 2.1 | SQL vs NoSQL — when each fits; tradeoffs (schema, scale, consistency) | STUDY | Can explain why we'd choose Postgres over DynamoDB for structured financial data |
| 2.2 | Indexing — B-tree, what a query planner does, cost of over-indexing | STUDY | Can explain why adding an index speeds reads but slows writes |
| 2.3 | Sharding / partitioning — horizontal split strategies, hot-key problem | STUDY | Can describe a shard key choice for a trades table and a failure mode |
| 2.4 | Replication — leader-follower, eventual consistency lag, read replicas | STUDY | Can explain the read-replica pattern and the stale-read risk |
| 2.5 | Caching — cache-aside vs write-through, eviction (LRU/TTL), stampede | SPINE | Add Redis caching for /ask responses; write ADR on what to cache and TTL choice |
| 2.6 | CDN — what it caches (static assets), what it cannot (dynamic API) | STUDY | Can explain why a CDN helps our static UI but not /ask |

---

## Block 3 — Communication Patterns

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 3.1 | REST design — resources, HTTP verbs, status codes, idempotency | STUDY | Can critique our current /ask API design (verb choice, status codes) |
| 3.2 | gRPC vs REST vs GraphQL — tradeoffs, when each fits | STUDY | Can say when you'd replace our REST endpoint with gRPC |
| 3.3 | Message queues — producer/consumer, at-least-once vs exactly-once | SPIKE | Tiny SQS or RabbitMQ demo: send a "question" message, consume + log it |
| 3.4 | Event-driven architecture — events vs commands, eventual consistency | STUDY | Can explain how /ask could become event-driven and what that buys |
| 3.5 | Pub/sub — fan-out, topic vs queue semantics | STUDY | Can distinguish SQS (queue) from SNS (pub/sub) [VERIFY: confirm we actually used SNS in Phase 4 before relying on this] |

---

## Block 4 — Reliability & Failure Design

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 4.1 | Retries + exponential backoff + jitter — why naive retry causes thundering herd | SPINE | Add retry + backoff to the Anthropic API call in the backend |
| 4.2 | Timeouts — why every network call needs one; where to set them | SPINE | Add explicit timeouts to the Anthropic SDK call and the Chroma query |
| 4.3 | Circuit breaker — closed/open/half-open states; when to use vs retry | STUDY | Can explain the difference between retry (transient) and circuit breaker (sustained) |
| 4.4 | Graceful degradation — returning a useful partial response on failure | SPINE | If Anthropic API is down, return cached answer or honest "unavailable" — not 500 |
| 4.5 | SPOF analysis — identify every single point of failure in the current arch | STUDY | Draw the current architecture and label every SPOF |
| 4.6 | Health checks — liveness vs readiness; what they should actually test | SPINE | Replace the dummy GET / with a real readiness check (Chroma + model loaded) |

---

## Block 5 — Scalability Patterns

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 5.1 | Load balancing — L4 vs L7, round-robin vs least-connections, sticky sessions | STUDY | Can explain why sticky sessions break horizontal scaling for stateless apps |
| 5.2 | Rate limiting — token bucket vs leaky bucket; where to enforce (gateway vs app) | SPINE | Add per-IP rate limiting to /ask (FastAPI middleware or slowapi) |
| 5.3 | Connection pooling — why opening a new DB connection per request is expensive | STUDY | Can explain what a connection pool is and what happens when it exhausts |
| 5.4 | CQRS — separate read and write models; when complexity is justified | STUDY | Can explain when CQRS is overkill (our app) vs necessary (high-write analytics) |
| 5.5 | Autoscaling — target tracking vs step; what metric to scale on for our app | STUDY | Can say what metric drives autoscaling for a CPU-bound vs I/O-bound service |

---

## Block 6 — API Design & Gateway

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 6.1 | API versioning — URL vs header, breaking vs non-breaking changes | STUDY | Can version our /ask endpoint and explain the migration path |
| 6.2 | API gateway — what it adds (auth, rate limit, routing) vs a reverse proxy | STUDY | Can explain what an API gateway gives us that nginx alone does not |
| 6.3 | Idempotency — why POST /ask is not idempotent and when that matters | STUDY | Can explain idempotency keys for payment APIs vs read-heavy RAG |
| 6.4 | Authentication patterns — JWT, OAuth2, API keys, RBAC | SPINE | Add API key authentication to /ask (header check, reject 401 without key) |

---

## Block 7 — Observability (beyond what we built)

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 7.1 | The three pillars — metrics, logs, traces; what each answers | STUDY | Can say which pillar answers "is it slow?" vs "what error happened?" |
| 7.2 | SLOs / SLAs / SLIs — definitions, error budgets | STUDY | Can write an SLO for /ask (e.g. p99 < 5s, 99.5% success rate) |
| 7.3 | Distributed tracing — trace ID, spans, why logs alone fail in microservices | STUDY | Can explain why a single trace_id per /ask request helps debug LLM latency |
| 7.4 | Structured logging — why key=value beats free-text for querying | SPINE | Convert logger.info("Question: %s") to structured JSON log with trace_id |

---

## Block 8 — Security (finance lens)

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 8.1 | Encryption at rest vs in transit — what each protects against | STUDY | Can explain what TLS protects (MITM) vs disk encryption (stolen hardware) |
| 8.2 | Secrets management — env vars vs Secrets Manager vs Vault; rotation | SPINE | Move ANTHROPIC_API_KEY from .env on EC2 to AWS Secrets Manager; fetch at startup |
| 8.3 | OWASP top 10 — injection, broken auth, insecure deserialization (finance lens) | STUDY | Can identify which OWASP risks apply to /ask (prompt injection is one) |
| 8.4 | Prompt injection — what it is, why it's the LLM equivalent of SQL injection | STUDY | Can write a test input that attempts prompt injection on our system prompt |

---

## Block 9 — Architecture Patterns

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 9.1 | Monolith vs modular monolith vs microservices — the spectrum | STUDY | Can place our app on the spectrum and explain the forcing functions to move right |
| 9.2 | Event sourcing — append-only log as source of truth, replay | STUDY | Can explain event sourcing for a trades ledger and the audit trail benefit |
| 9.3 | Saga pattern — distributed transactions without a 2PC lock | STUDY | Can describe a saga for a multi-step leaver process (trigger -> confirm -> archive) |
| 9.4 | Strangler fig — incremental migration from monolith | STUDY | Can explain how to extract the /ask endpoint from a hypothetical monolith |
| 9.5 | ADRs + C4 diagrams — how architects document decisions and communicate systems | SPINE | Write 2 ADRs for decisions already made (RAG backend choice, Docker deploy) |

---

## Block 10 — AI / LLM Architecture (the layer on top)

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 10.1 | RAG vs fine-tuning — when each fits, cost/freshness tradeoffs | STUDY | Can explain why we chose RAG and under what conditions fine-tuning wins |
| 10.2 | Guardrails — input validation, output validation, refusal handling | SPINE | Add input length limit + output content check to /ask |
| 10.3 | Cost control — token budgets, caching, model tier selection | STUDY | Can estimate monthly Claude API cost at 1000 queries/day and propose 3 cuts |
| 10.4 | Evals at scale — automated quality regression for LLM outputs | SPINE | Extend the eval script to run against 20 golden Q&A pairs and report pass rate |
| 10.5 | Prompt injection (LLM-specific) — detection and mitigation patterns | STUDY | See 8.4 |

---

## Block 11 — Infrastructure Spikes (breadth: your explicit list)

Heavy patterns that do NOT fit the single spine app. Learned as ISOLATED spikes
or study, NEVER force-fit onto the policy-QA app. The rule: our app is one
low-traffic container — it genuinely needs NONE of these, and being able to say
"this doesn't need K8s, here's why" IS the architect skill being graded.

| # | Topic | Track | Done bar |
|---|-------|-------|----------|
| 11.1 | Containers at scale / Kubernetes — pods, services, deployments, when it's overkill | SPIKE | Deploy 2 dummy containers to a local cluster (kind/minikube); see pods+service route traffic. Paragraph: what K8s solves + why our app does NOT need it |
| 11.2 | VPC / networking — subnets (public vs private), route tables, security groups | STUDY | Can draw a VPC with public+private subnets and place our EC2 correctly; explain what's exposed |
| 11.3 | NAT gateway — why private-subnet resources need it, and what it costs | STUDY | Can explain why NAT exists and why adding it "to look real" is a cost trap for our app |
| 11.4 | Load balancer (hands-on) — optional spike on top of 5.1 | SPIKE (optional) | 2 dummy instances behind an ALB; watch traffic distribute. Only if time allows |

---

## Final deliverables (these prove Phase 5)

### Deliverable 1 — "Scale this to 10x" design doc (the spine)
Our app currently handles ~10 queries/day on one EC2. Design it for 10,000/day.
Cover:
- Where it breaks first (SPOF, bottleneck)
- What you'd change and why (load balancer, caching, async queue, read replica)
- What you'd NOT change yet and why (the restraint — the architect signal)
- Two ADRs for the biggest decisions made

### Deliverable 2 — AI-analytics-SaaS design case study (PAPER ONLY — do NOT build)
Architect (on paper) an AI analytics SaaS: text-to-SQL over structured business
data (LLM -> NL-to-SQL -> execute -> LLM explains), with RAG used for SCHEMA /
semantic-layer retrieval (NOT row data), multi-tenancy, ingestion (messy Excel)
OR connect-to-existing-DB as a smaller wedge, SQL validation, cost, security,
and where AI must NOT decide. Produce: component diagram, data flow, key
tradeoffs, 1-2 ADRs.
- Purpose here = architecture reps + a portfolio case study + pressure-testing
  the idea's real complexity. It is NOT a product build.
- BUILD-OR-NOT decision is PARKED until after Phase 6. Before any commercial
  build: (1) check SS&C employment contract (moonlighting/IP/conflict),
  (2) validate the "connect to existing DB" wedge with a few real users,
  (3) confirm the plan is finished first. Do NOT let this replace the plan.

---

## Carried decisions / parked items

- ML System Design (interview genre): parked — decide vs target roles.
- DSA sprint: only if a target company screens for it.
- Geo + cert target: decide at Phase 6.
- PHASE 6 OPTIONAL CERT: Claude Certified Architect – Foundations (Anthropic,
  verified real). Vendor-specific (certifies the AI layer, ~20% of the general
  architect target) — complements, does NOT replace, general system-design proof.
  Low marginal cost (plan already covers most). Decide in Phase 6 with the
  geo/cert call. Resources: anthropic.skilljar.com (free courses);
  github.com/anthropics/claude-cookbooks; modelcontextprotocol.io;
  platform.claude.com/docs; anthropic-partners.skilljar.com (exam blueprint /
  register — may be partner-network-gated, verify access at Phase 6);
  claude.com/partners.

---

## Tracking

Mark each row DONE as it's completed. Update TRACKER.md at end of each session.
Sequence is vocabulary-first: Block 1 fully before moving on, then in order.

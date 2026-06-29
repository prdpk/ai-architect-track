# Design Note — Trade Analysis Tool

**Status:** Accepted

## Context

A small tool reads synthetic trade data from a CSV file and produces an analysis
that combines computed metrics with a short natural-language summary. The central
design question: **which work should be done in deterministic code, and which
should be delegated to the LLM?**

## Decision

Compute all numeric values (trade counts, buy/sell counts, total quantity) in
**Python**. Use the LLM (Claude Haiku) **only** to generate the natural-language
summary. Assemble both into the final result.

## Reasoning

Code produces deterministic, verifiable results for calculations. LLMs are better
suited to generating readable text but can make mistakes when performing
arithmetic. During development this was not hypothetical: when the model was asked
to compute the totals, it reported a total quantity of **235** when the correct,
code-computed value was **275**. Keeping computation in code guarantees
correctness; the LLM handles only language, which is where it adds value.

**Rule:** numbers from code, words from the model.

## Benefits

* Numeric results are always correct and reproducible.
* The LLM is responsible only for language generation.
* The system is easier to test, because business logic is separated from
  AI-generated text.

## Tradeoffs Accepted

### 1. The summary is not deterministic

The natural-language summary may vary between runs, even on identical data. This
is acceptable because the summary exists to improve readability, not to serve as a
source of truth. All numeric values are computed in Python, so the important
business data remains accurate and verifiable.

### 2. Additional cost and latency

Calling the LLM introduces API cost and network latency that a pure-Python
solution would not have. Accepted because generating human-friendly summaries is a
task where the LLM adds genuine value, while the numeric calculations stay
efficient and deterministic in Python.

### 3. Higher token usage

The current implementation sends all trade rows to the LLM so it has full context
for the summary. This increases token usage and cost. For a small demonstration
this is acceptable in exchange for simplicity; in a production system I would send
only the computed facts or a compact representation of the trades to cut token
usage and cost.

## What I'd Change at Scale

### 1. Send less data to the LLM

Instead of every trade row, send only what the summary needs (symbols traded,
whether buying or selling dominated). Fewer input tokens → lower cost and faster
responses.

### 2. Cache repeated summaries

If the same trade data is analyzed more than once, cache the generated summary and
reuse it instead of calling the LLM again — reducing API cost and improving
performance for repeated requests.

### 3. Replace the CSV with a database

A CSV works for a small project but does not scale to large datasets or concurrent
users. A database would make the data easier to query and update, and would
support multiple users or services at once.

# AI Architect Track

## Overview

This project demonstrates a simple AI-assisted trade analysis workflow.

The application:

* Loads trade data from a CSV file.
* Computes all numeric metrics (trade counts and quantities) using Python.
* Uses Anthropic Claude Haiku to generate a short natural-language summary of the trading activity.
* Combines the computed metrics and AI-generated summary into a final result.

This architecture ensures that calculations remain deterministic and accurate while the LLM is used only for language generation.

---

## Prerequisites

Before running the project, ensure you have:

* Python 3.11 or later
* Git
* An Anthropic API key with available API credits

---

## Installation

Clone the repository using HTTPS:

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

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Set your Anthropic API key as an environment variable.

macOS/Linux:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Windows PowerShell:

```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

---

## Project Structure

```text
ai-architect-track/
│
├── data/
│   └── trades.csv
│
├── scripts/
│   ├── summarize.py
│   └── analyze_trades.py
│
├── requirements.txt
└── README.md
```

---

## Running the Project

`analyze_trades.py` imports from `summarize.py`:

```python
from summarize import load_trades, summarize_trades, csv_path
```

Because of this import, change into the `scripts` directory before running it:

```bash
cd scripts
python3 analyze_trades.py
```

To run the pure-Python summary instead (no API key needed, no cost — useful for verifying your setup before spending any API credit):

```bash
cd scripts
python3 summarize.py
```

---

## Expected Output

Example output from `analyze_trades.py`:

```text
{
    "total_trades": 10,
    "buy_count": 6,
    "sell_count": 4,
    "total_quantity": 275,
    "summary": "The trading activity included purchases and sales across AAPL, MSFT, GOOG, and NVDA, with buying activity outweighing selling."
}

Usage:
Usage(input_tokens=..., output_tokens=...)
```

---

## Limitations

* Requires `data/trades.csv` to be present.
* Requires a valid Anthropic API key.
* Makes a paid API call to Anthropic (a fraction of a cent per run on Claude Haiku).
* Uses synthetic trade data for demonstration purposes only — no real trading logic or data.
* The AI generates only the natural-language summary. All numeric values are computed in Python.

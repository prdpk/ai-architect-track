import json
import anthropic
from summarize import load_trades, summarize_trades, csv_path

# Create the Anthropic client
client = anthropic.Anthropic()

try:
    # Load the trades from the CSV
    trades = load_trades(csv_path)

    # Compute all numbers in Python
    total_trades, buy_count, sell_count, total_quantity = summarize_trades(trades)

    # Convert trades to text for the prompt
    trade_rows = "\n".join(
        f'{t["date"]},{t["symbol"]},{t["side"]},{t["quantity"]},{t["price"]}'
        for t in trades
    )

    # Build the prompt
    prompt = f"""
Here are some trades:

{trade_rows}

Write one short plain-English sentence describing the trading activity.

Mention:
- which symbols were traded
- the overall buying and selling activity

Do NOT output counts, totals, quantities, prices, or any numbers.
Return only the sentence.
"""

    # Call Claude Haiku
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    summary = message.content[0].text.strip()

    # Assemble the final result in Python
    result = {
        "total_trades": total_trades,
        "buy_count": buy_count,
        "sell_count": sell_count,
        "total_quantity": total_quantity,
        "summary": summary,
    }

    print(result)

    print("\nUsage:")
    print(message.usage)

except FileNotFoundError:
    print(f"Error: '{csv_path}' does not exist.")
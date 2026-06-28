import anthropic

client = anthropic.Anthropic()

# Step 1: Define the trade rows as embedded text
trade_rows = """\
2026-01-03,AAPL,BUY,50,191.25
2026-01-03,MSFT,BUY,30,402.10
2026-01-05,AAPL,SELL,20,195.80
"""

# Step 2: Build the prompt
prompt = f"""
Here are 3 trades.

return ONLY a JSON object with these exact keys — e.g. total_trades, buy_count, sell_count, total_quantity, and a short summary string. Be explicit: "Respond with only the JSON, no other text.

Trades:
{trade_rows}
"""

# Step 3: Call Claude Haiku
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

# Step 4: Print the summary
print("Summary:\n")
print(message.content[0].text)

# Step 5: Print token usage
print("\nUsage:")
print(message.usage)
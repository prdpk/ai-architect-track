import json
import anthropic

# Create the Anthropic client
client = anthropic.Anthropic()

# Step 1: Define the trade rows as embedded text
trade_rows = """\
2026-01-03,AAPL,BUY,50,191.25
2026-01-03,MSFT,BUY,30,402.10
2026-01-05,AAPL,SELL,20,195.80
2026-01-06,GOOG,BUY,15,141.55
2026-01-08,MSFT,SELL,30,410.00
2026-01-09,NVDA,BUY,40,128.90
2026-01-10,AAPL,BUY,25,188.40
2026-01-12,GOOG,SELL,15,139.20
2026-01-13,NVDA,SELL,40,134.65
2026-01-15,MSFT,BUY,10,415.30
"""

# Step 2: Build the prompt
prompt = f"""
Here are some trades.

Return ONLY a JSON object with these exact keys:
- total_trades
- buy_count
- sell_count
- total_quantity
- summary

Respond with only the JSON object and no other text.
Do NOT wrap the JSON in markdown.
Do NOT use ```json.
Do NOT include any explanation or extra text.

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

# Step 4: Get the JSON response
response_text = message.content[0].text

print("Raw response:")
print(repr(response_text))

# Step 5: Parse the JSON
data = json.loads(response_text)

# Step 6: Print the parsed data
print("Parsed JSON:")
print(data)

print("\nTotal Quantity:")
print(data["total_quantity"])

print("\nSummary:")
print(data["summary"])

# Step 7: Print token usage
print("\nUsage:")
print(message.usage)
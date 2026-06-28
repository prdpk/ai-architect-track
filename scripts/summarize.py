import csv
from pathlib import Path

here = Path(__file__).resolve().parent
csv_path = here.parent / "data" / "trades.csv"


def load_trades(path):
    with open(path, "r") as file:
        csv_reader = csv.DictReader(file)

        rows = []
        for row in csv_reader:
            rows.append(row)

    return rows


def print_trades(rows):
    for row in rows:
        print(
            f'\t on {row["date"]} I trade for {row["symbol"]} '
            f'with quantity {row["quantity"]} and with price of {row["price"]}.'
        )


def summarize_trades(rows):
    trade_count = 0
    buy_count = 0
    sell_count = 0
    total_quantity = 0

    for row in rows:
        if row["side"] == "BUY":
            buy_count += 1
        elif row["side"] == "SELL":
            sell_count += 1

        total_quantity += int(row["quantity"])
        trade_count += 1

    return trade_count, buy_count, sell_count, total_quantity


if __name__ == "__main__":
    try:
        trades = load_trades(csv_path)

        print(trades[0].keys())
        print_trades(trades)

        trade_count, buy_count, sell_count, total_quantity = summarize_trades(trades)

        print(f"Processed total {trade_count} trade.")
        print(f"Buy side count is {buy_count}.")
        print(f"Sell side count is {sell_count}.")
        print(f"Total quantity is {total_quantity}.")

    except FileNotFoundError:
        print("The file does not exist.")
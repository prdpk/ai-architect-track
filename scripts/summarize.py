import csv
from pathlib import Path

here = Path(__file__).resolve().parent
csv_path = here.parent / "data" / "trades.csv"

try:
    with open(csv_path, "r") as file:
        csv_reader = csv.DictReader(file)
        trade_count = 0
        buy_count = 0
        sell_count = 0
        total_quantity = 0
        print(csv_reader.fieldnames)
        for row in csv_reader:
            print(f'\t on {row["date"]} I trade for {row["symbol"]} with quantity {row["quantity"]} and with price of {row["price"]}.')
            if row["side"] == "BUY":
                buy_count += 1
            else:
                sell_count += 1
            total_quantity += int(row["quantity"])
            trade_count += 1
        print(f'Processed total {trade_count} trade.')
        print(f'Buy side count is {buy_count}.')
        print(f'Sell side count is {sell_count}.')
        print(f'Total quantity is {total_quantity}.')
except FileNotFoundError:
    print("The file does not exist.")
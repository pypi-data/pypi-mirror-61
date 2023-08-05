import csv
import os
from collections import defaultdict

import click
import dateparser


def process_amount(amount):
    if amount:
        return float(amount.replace(",", "."))
    return ""


def process_memo(line):
    return " - ".join(
        filter(None, map(str.strip, [line["Category"], line["Exchange Rate"]]))
    )


@click.command()
@click.argument("csv_filename")
@click.option(
    "--ynab/--file",
    default=False,
    help="Push data directly to YNAB instead of writing a file.",
)
def cli(csv_filename, ynab):
    formatted_data = []
    ynab_transactions = []
    transaction_ids = defaultdict(int)

    with open(csv_filename) as f:
        reader = csv.DictReader(f, delimiter=";")
        for line in reader:
            date = dateparser.parse(line["Completed Date"]).strftime("%Y-%m-%d")
            payee = line["Reference"]
            memo = process_memo(line)
            outflow = process_amount(line["Paid Out (EUR)"])
            inflow = process_amount(line["Paid In (EUR)"])
            formatted_data.append(
                {
                    "Date": date,
                    "Payee": payee,
                    "Memo": memo,
                    "Outflow": outflow,
                    "Inflow": inflow,
                }
            )
            amount = outflow if outflow else inflow
            amount *= 1000
            import_id = f"YNAB:{amount}:{date}"
            transaction_ids[import_id] += 1
            occurrence = transaction_ids[import_id]
            import_id = f"{import_id}:{occurrence}"
            ynab_transactions.append(
                {
                    "date": date,
                    "amount": amount,
                    "payee_name": payee,
                    "memo": memo,
                    "import_id": import_id,
                }
            )

    if not formatted_data:
        click.secho("Nothing to write.")

    if ynab:
        ynab.push_transactions(ynab_transactions, "revolut")
    else:
        processed_file = os.path.join(os.path.dirname(csv_filename), "processed.csv")
        with open(processed_file, "w") as f:
            writer = csv.DictWriter(
                f, delimiter=",", quotechar='"', fieldnames=formatted_data[0].keys()
            )
            writer.writeheader()
            writer.writerows(formatted_data)

            click.secho("{} written".format(processed_file), fg="green")


if __name__ == "__main__":
    cli()

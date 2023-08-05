import os
import re
import sys
from collections import defaultdict
from xml.etree import ElementTree

import click
from ofxtools.Parser import OFXTree
from ofxtools.header import make_header

from ofx_processor.utils import ynab


@click.command()
@click.argument("ofx_filename")
@click.option(
    "--ynab/--file",
    "push_to_ynab",
    default=False,
    help="Push data directly to YNAB instead of writing a file.",
)
def cli(ofx_filename, push_to_ynab):
    parser = OFXTree()
    try:
        parser.parse(ofx_filename)
    except FileNotFoundError:
        click.secho("Couldn't open ofx file", fg="red")
        sys.exit(1)

    ofx = parser.convert()

    if ofx is None:
        click.secho("Couldn't parse ofx file", fg="red")
        sys.exit(1)

    ynab_transactions = []
    transaction_ids = defaultdict(int)

    for transaction in ofx.statements[0].transactions:
        if "CB****" in transaction.name:
            name = transaction.name
            memo = transaction.memo
            conversion = re.compile(r"\d+,\d{2}[a-zA-Z]{3}")
            match = conversion.search(memo)
            if match:
                transaction.name = memo[: match.start() - 1]
                transaction.memo = name + memo[match.start() - 1 :]
            else:
                transaction.name = memo
                transaction.memo = name

            click.secho(
                "Edited transaction {} ({})".format(
                    transaction.checknum, transaction.name
                ),
                fg="blue",
            )

        date = transaction.dtposted.isoformat().split("T")[0]
        amount = int(transaction.trnamt * 1000)
        import_id = f"YNAB:{amount}:{date}"
        transaction_ids[import_id] += 1
        occurrence = transaction_ids[import_id]
        import_id = f"{import_id}:{occurrence}"

        ynab_transactions.append(
            {
                "date": date,
                "amount": amount,
                "payee_name": transaction.name,
                "memo": transaction.memo,
                "import_id": import_id,
            }
        )
    click.secho(f"Processed {len(ynab_transactions)} transactions total.", fg="blue")

    if push_to_ynab:
        ynab.push_transactions(ynab_transactions, "bpvf")
    else:
        header = str(make_header(version=102))
        root = ofx.to_etree()
        data = ElementTree.tostring(root).decode()
        processed_file = os.path.join(os.path.dirname(ofx_filename), "processed.ofx")
        with open(processed_file, "w") as f:
            f.write(header + data)
            click.secho("{} written".format(processed_file), fg="green")


if __name__ == "__main__":
    cli()

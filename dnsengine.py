from typing import Optional

import click

from src.fetcher import get_records, get_record, get_record_to_json


@click.command()
@click.argument('domain')
@click.option('-t', '--rtype', type=str, help='DNS record type to search')
@click.option('-b', '--blob', type=str, help='Output to json file')
def app(domain: str, rtype: Optional[str], blob: Optional[str]):
    if rtype:
        # if type provided, return only the specific type
        answer = get_record(domain_string=domain, record_type=rtype)
        click.echo(answer)
    elif blob:
        get_record_to_json(domain_string=domain, file_name=blob)

    else:
        answer = get_records(domain_string=domain)
        click.echo(answer)


if __name__ == "__main__":
    app()

from typing import Optional

import click

from src.fetcher import get_records, get_record


@click.command()
@click.argument('domain')
@click.option('-t', '--rtype', type=str, help='DNS record type to search')
def app(domain: str, rtype: Optional[str]):
    # if type provided, return only the specific type
    answer = get_record(domain_string=domain, record_type=rtype) if rtype else get_records(domain_string=domain)
    click.echo(answer)


if __name__ == "__main__":
    app()

import click

from src.fetcher import get_records, get_record


@click.command()
@click.argument('domain')
@click.option('-t', '--rtype', type=str)
def app(domain, rtype: str):
    if rtype:
        # if type provided, return only the specific type
        answer = get_record(domain_string=domain, record_type=rtype)
        click.echo(answer)
    else:
        answer = get_records(domain_string=domain)
        click.echo(answer)


if __name__ == "__main__":
    app()

import click

from app.commits.commits import query


@click.group()
def commits():
    """
    Commit Management Commands
    """
    pass


commits.add_command(query)

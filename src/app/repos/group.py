import click

from app.repos.repos import create, ls, delete


@click.group()
def repos():
    """
    Repository Management Commands
    """
    pass


repos.add_command(create)
repos.add_command(ls)
repos.add_command(delete)

import click

from app.files.files import history


@click.group()
def files():
    """
    File Management Commands
    """
    pass


files.add_command(history)

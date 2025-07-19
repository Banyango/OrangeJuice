import sys
import click

from app.container import Container
from app.repos.repos import ls, create


@click.group()
def cli():
    """
    OrangeJuice CLI Application
    """
    pass


container = Container()
container.init_resources()

cli.add_command(create)
cli.add_command(ls)

if __name__ == "__main__":
    cli()

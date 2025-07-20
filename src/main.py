import click

from app.container import Container
from app.repos.repos import ls, create, delete


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
cli.add_command(delete)

if __name__ == "__main__":
    cli()

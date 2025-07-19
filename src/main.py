import click

from app.container import Container
from app.repos.repos import ls, create


class App:
    def __init__(self):
        container = Container()
        container.init_resources()



@click.group()
def cli():
    """
    OrangeJuice CLI Application
    """
    pass


cli.add_command(create)
cli.add_command(ls)

if __name__ == "__main__":
    cli()
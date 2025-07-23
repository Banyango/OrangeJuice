import click

from app.repos.group import repos
from app.commits.group import commits

from app.container import Container


@click.group()
def cli():
    """
    OrangeJuice CLI Application
    """
    pass


container = Container()
container.init_resources()

cli.add_command(repos)
cli.add_command(commits)

if __name__ == "__main__":
    cli()

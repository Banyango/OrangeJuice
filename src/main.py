import click

from app.config import AppConfig
from app.repos.group import repos
from app.commits.group import commits

from container import ApplicationContainer


@click.group()
def cli():
    """
    OrangeJuice CLI Application
    """
    pass


container = ApplicationContainer()
container.init_resources()

cli.add_command(repos)
cli.add_command(commits)

if __name__ == "__main__":
    cli()

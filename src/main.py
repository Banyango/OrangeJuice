import click

from app.container import Container

from app.repos.group import repos
from app.commits.group import commits


@click.group()
def cli():
    """
    OrangeJuice CLI Application
    """
    pass


container = Container()
container.wire(modules=[__name__])
container.init_resources()

cli.add_command(repos)
cli.add_command(commits)

if __name__ == "__main__":
    cli()

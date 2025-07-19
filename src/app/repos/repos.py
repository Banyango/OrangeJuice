import click

from app.container import Container
from app.repos.responses import RepoResponseModel
from core.repos.add_repo_operation import AddRepoOperation

from dependency_injector.wiring import Provide, inject

from data.repos.queries import RepoQueries


@click.command()
@inject
def ls(queries: Provide[RepoQueries]) -> list:
    """
    Returns a list of repositories.
    """
    repos = queries.get_repos()

    if not repos:
        return []

    return [
        RepoResponseModel(name=repo.name)
        for repo in repos
    ]

@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.command(name='create')
def create(path:str, operation: AddRepoOperation = Provide[Container.add_repo_operation]) -> None:
    """
    Creates a new repository.

    Args:
        path (str): The path to the repository.
        operation (AddRepoOperation): The operation to add a repository.
    """
    operation.execute(path)



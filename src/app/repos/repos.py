import click

from app.container import Container
from app.repos.responses import RepoResponseModel
from core.repos.add_repo_operation import AddRepoOperation
from data.repos.queries import RepoQueries

from dependency_injector.wiring import Provide, inject


@click.command()
def ls(repo_queries: RepoQueries) -> list:
    """
    Returns a list of repositories.

    Args:
        repo_queries (RepoQueries): The queries to fetch repositories.
    """
    repos = repo_queries.get_repos()

    if not repos:
        return []

    return [RepoResponseModel(name=repo.name) for repo in repos]


@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.command()
@inject
def create(
    path: str,
    add_repo_operation: AddRepoOperation = Provide[Container.add_repo_operation],
) -> None:
    """
    Creates a new repository.

    Args:
        path (str): The path to the repository.
        add_repo_operation (AddRepoOperation): The operation to add a repository.
    """
    add_repo_operation.execute(path)

import click
from loguru import logger

from app.container import Container
from app.repos.responses import RepoResponseModel
from core.repos.add_repo_operation import AddRepoOperation
from core.repos.errors import RepoAlreadyExistsError
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
@click.argument("name", type=str)
@click.command()
@inject
def create(
    path: str,
    name: str,
    add_repo_operation: AddRepoOperation = Provide[Container.add_repo_operation],
) -> None:
    """
    Creates a new repository.

    Args:
        path (str): The path to the repository.
        name (str): The name of the repository.
        add_repo_operation (AddRepoOperation): The operation to add a repository.
    """
    try:
        add_repo_operation.execute(path, name)
    except RepoAlreadyExistsError:
        logger.error(f"Repository '{name}' already exists.")

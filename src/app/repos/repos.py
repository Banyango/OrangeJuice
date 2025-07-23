import click
from loguru import logger

from app.container import Container

from core.repos.add_repo_operation import AddRepoOperation
from core.repos.delete_repo_operation import DeleteRepoOperation
from core.repos.errors import RepoAlreadyExistsError
from data.repos.queries import RepoQueries

from dependency_injector.wiring import Provide, inject


@click.command()
@inject
def ls(repo_queries: RepoQueries = Provide[Container.repo_queries]) -> None:
    """
    Returns a list of repositories.

    Args:
        repo_queries (RepoQueries): The queries to fetch repositories.
    """
    repos = repo_queries.get_repos()

    if not repos:
        logger.info("No repositories found.")

    for repo in repos:
        logger.info(f"Repository: {repo.name}, Path: {repo.path}")


@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
@click.option("--name", type=str, required=True)
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


@click.option("--name", type=str, required=True)
@click.command()
@inject
def delete(
    name: str,
    delete_repo_operation: DeleteRepoOperation = Provide[
        Container.delete_repo_operation
    ],
) -> None:
    """
    Deletes a repository.

    Args:
        name (str): The name of the repository.
        delete_repo_operation (DeleteRepoOperation): The operation to delete a repository.
    """
    delete_repo_operation.execute(name)

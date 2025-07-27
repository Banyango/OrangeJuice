import click
from loguru import logger

from app.container import Container
from core.files.queries.queries import FilesQueries

from dependency_injector.wiring import Provide, inject


@click.option('--name', type=str, required=True)
@click.option('--file', type=str, required=True)
@click.command()
@inject
def history(
        name: str = None,
        file: str = None,
        file_queries: FilesQueries = Provide[Container.core.file_queries]) -> None:
    """
    Returns a list of repositories.

    Args:
        name (str): The name of the repository.
        file (str): The path to the file within the repository.
        file_queries (RepoQueries): The queries to fetch repositories.
    """
    files = file_queries.get_file_history(file, name)

    if not files:
        logger.info("No file history found.")

    for file in files:
        logger.info(f"Commit: {file['commit']}, Message: {file['message']}, Author: {file['author']}, Date: {file['date']}")

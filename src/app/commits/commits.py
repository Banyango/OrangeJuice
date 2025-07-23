import click
from dependency_injector.wiring import Provide, inject
from loguru import logger

from app.container import Container
from data.commits.queries import CommitQueries


@click.option("--name", type=str, required=True)
@click.option("--query", type=str, required=True)
@click.command()
@inject
def query(
    name: str,
    query: str,
    commit_queries: CommitQueries = Provide[Container.commit_queries],
) -> None:
    """
    Creates a new repository.

    Args:
        name (str): The name of the repository.
        query (str): The query to search for in the commit messages.
        commit_queries (RepoQueries): The queries to fetch repositories.
    """
    if len(query) < 8:
        logger.warning(
            "Short query string may not work well with chroma's default embedding model."
        )

    results = commit_queries.query_by_commit_message(name, query)

    if not results:
        logger.info(f"No repositories found for commit message: {name}")
        return

    for result in results[0]:
        click.echo(result.strip())

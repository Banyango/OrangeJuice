from dependency_injector import containers, providers

from core.repos.add_repo_operation import AddRepoOperation
from data.repos.queries import RepoQueries
from libs.duckdb.provider import DuckDbClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # DuckDB Client
    duckdb_client = providers.Singleton(
        DuckDbClient,
        config=config.duckdb
    )

    # operations
    add_repo_operation = providers.Factory(
        AddRepoOperation,
        duckdb_client=duckdb_client
    )

    # queries
    repo_queries = providers.Factory(
        RepoQueries,
        duckdb_client=duckdb_client
    )
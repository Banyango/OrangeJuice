from dependency_injector import containers, providers

from app.config import AppConfig
from core.repos.add_repo_operation import AddRepoOperation
from data.repos.queries import RepoQueries
from libs.duckdb.provider import DuckDbClient
from dotenv import load_dotenv

load_dotenv()

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.repos",
            "data.repos",
            "core.repos",
            "libs.duckdb",
        ],
    )

    # AppConfig
    app_config = providers.Singleton(
        AppConfig
    )

    # DuckDB Client
    duckdb_client = providers.Singleton(
        DuckDbClient,
        app_config=app_config,
    )

    # operations
    add_repo_operation = providers.Factory(
        AddRepoOperation, duckdb_client=duckdb_client
    )

    # queries
    repo_queries = providers.Factory(RepoQueries)

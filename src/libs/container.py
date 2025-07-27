from dependency_injector import containers, providers

from app.config import AppConfig
from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "libs.duckdb",
            "libs.chromadb",
        ],
    )

    app_config = providers.Singleton(
        AppConfig,
    )

    # Chroma Client
    search_client = providers.Singleton(
        ChromaClient,
        app_config=app_config,
    )

    # Query client
    query_client = providers.Singleton(
        DuckDbClient,
        app_config=app_config,
    )

from dependency_injector import containers, providers

from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient
from libs.embeddings.provider import EmbeddingClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.DependenciesContainer()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "libs.duckdb",
            "libs.chromadb",
        ],
    )

    # Embedding Client
    embedding_client = providers.Singleton(
        EmbeddingClient,
        app_config=core.app_config,
    )

    # Chroma Client
    core.search_client.override(
        providers.Singleton(
            ChromaClient,
            app_config=core.app_config,
        ),
    )

    # Query client
    core.query_client.override(
        providers.Singleton(
            DuckDbClient,
            app_config=core.app_config,
        ),
    )

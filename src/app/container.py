from dependency_injector import containers, providers

from app.config import AppConfig
from app.embeddings.embedding_function import CustomEmbeddingFunction
from core.repos.add_repo_operation import AddRepoOperation
from data.repos.queries import RepoQueries
from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient
from dotenv import load_dotenv

from libs.embeddings.provider import EmbeddingClient

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

    # Embedding Client
    embedding_client = providers.Singleton(
        EmbeddingClient,
        app_config=app_config,
    )

    # Chroma Client
    embedding_function = providers.Factory(
        CustomEmbeddingFunction,
        embedding_client=embedding_client
    )
    chroma_client = providers.Singleton(
        ChromaClient,
        app_config=app_config,
        embedding_function=embedding_function
    )

    # DuckDB Client
    duckdb_client = providers.Singleton(
        DuckDbClient,
        app_config=app_config,
    )

    # operations
    add_repo_operation = providers.Factory(
        AddRepoOperation,
        duckdb_client=duckdb_client,
        embedding_client=embedding_client,
    )

    # queries
    repo_queries = providers.Factory(RepoQueries)

from dependency_injector import containers, providers

from app.config import AppConfig
from app.embeddings.embedding_function import CustomEmbeddingFunction
from core.repos.add_repo_operation import AddRepoOperation
from core.repos.delete_repo_operation import DeleteRepoOperation
from data.repos.queries import RepoQueries
from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient
from dotenv import load_dotenv

from libs.embeddings.provider import EmbeddingClient

load_dotenv()


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the OrangeJuice application.
    """

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
    app_config = providers.Singleton(AppConfig)

    # Embedding Client
    embedding_client = providers.Singleton(
        EmbeddingClient,
        app_config=app_config,
    )

    # Chroma Client
    embedding_function = providers.Factory(
        CustomEmbeddingFunction,
        app_config=app_config,
        embedding_client=embedding_client,
    )
    chroma_client = providers.Singleton(
        ChromaClient, app_config=app_config, embedding_function=embedding_function
    )

    # DuckDB Client
    duckdb_client = providers.Singleton(
        DuckDbClient,
        app_config=app_config,
    )

    # ==== Operations =====

    # Repo
    add_repo_operation = providers.Factory(
        AddRepoOperation,
        duckdb_client=duckdb_client,
        chromadb_client=chroma_client,
    )

    delete_repo_operation = providers.Factory(
        DeleteRepoOperation,
        duckdb_client=duckdb_client,
        chroma_client=chroma_client,
    )

    # queries
    repo_queries = providers.Factory(RepoQueries)

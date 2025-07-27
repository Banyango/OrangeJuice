from dependency_injector import containers, providers

from app.config import AppConfig
from core.repos.operations.add_repo_operation import AddRepoOperation
from core.repos.operations.delete_repo_operation import DeleteRepoOperation
from core.repos.operations.update_repo_operation import UpdateRepoOperation
from core.commits.queries.queries import CommitQueries
from core.repos.queries.queries import RepoQueries
from dotenv import load_dotenv

load_dotenv()


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the OrangeJuice application.
    """
    config = providers.Configuration()

    libs = providers.DependenciesContainer()

    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.repos",
            "app.commits",
            "core.repos",
            "core.commits"
        ],
    )

    # ==== AppConfig =====

    app_config = providers.Singleton(AppConfig)

    # ===== Operations =====

    # Repo
    add_repo_operation = providers.Factory(
        AddRepoOperation,
        query_client=libs.query_client,
        search_client=libs.search_client,
    )

    delete_repo_operation = providers.Factory(
        DeleteRepoOperation,
        query_client=libs.query_client,
        search_client=libs.search_client,
    )

    update_repo_operation = providers.Factory(
        UpdateRepoOperation,
        query_client=libs.query_client,
        search_client=libs.search_client,
    )

    # Queries
    repo_queries = providers.Factory(
        RepoQueries,
        query_client=libs.query_client,
        search_client=libs.search_client,
    )

    commit_queries = providers.Factory(
        CommitQueries,
        query_client=libs.query_client,
        search_client=libs.search_client,
    )

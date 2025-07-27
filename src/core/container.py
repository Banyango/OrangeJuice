from dependency_injector import containers, providers

from app.config import AppConfig
from core.commits.queries.queries import CommitQueries
from core.interfaces.query_client import QueryClient
from core.interfaces.search_client import SearchClient
from core.repos.operations.add_repo_operation import AddRepoOperation
from core.repos.operations.delete_repo_operation import DeleteRepoOperation
from core.repos.operations.update_repo_operation import UpdateRepoOperation
from core.repos.queries.queries import RepoQueries


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the OrangeJuice application.
    """
    config = providers.Configuration()

    app_config = providers.Singleton(AppConfig)

    query_client: providers.Provider[QueryClient] = providers.AbstractSingleton(
        instance_of=QueryClient,
        app_config=app_config,
    )

    search_client: providers.Provider[SearchClient] = providers.AbstractSingleton(
        instance_of=SearchClient,
        app_config=app_config,
    )

    # Repo
    add_repo_operation = providers.Factory(
        AddRepoOperation,
        query_client=query_client,
        search_client=search_client,
    )

    delete_repo_operation = providers.Factory(
        DeleteRepoOperation,
        query_client=query_client,
        search_client=search_client,
    )

    update_repo_operation = providers.Factory(
        UpdateRepoOperation,
        query_client=query_client,
        search_client=search_client,
    )

    # Queries
    repo_queries = providers.Factory(
        RepoQueries,
        query_client=query_client,
        search_client=search_client,
    )

    commit_queries = providers.Factory(
        CommitQueries,
        query_client=query_client,
        search_client=search_client,
    )

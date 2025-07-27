from dependency_injector import containers, providers

from core.interfaces.query_client import QueryClient
from core.interfaces.search_client import SearchClient


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the OrangeJuice application.
    """
    config = providers.Configuration()

    app = providers.DependenciesContainer()

    query_client: providers.Provider[QueryClient] = providers.AbstractSingleton(
        QueryClient,
        app_config=app.app_config,
    )

    search_client: providers.Provider[SearchClient] = providers.AbstractSingleton(
        SearchClient,
        app_config=app.app_config,
    )
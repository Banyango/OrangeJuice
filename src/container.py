from dependency_injector import containers, providers

from app.container import Container as AppContainer
from core.container import Container as CoreContainer
from libs.container import Container as LibsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(
        CoreContainer,
        config=config,
    )

    libs = providers.Container(
        LibsContainer,
        config=config,
    )

    app = providers.Container(
        AppContainer,
        config=config,
    )

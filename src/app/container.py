from dependency_injector import containers, providers

from app.config import AppConfig
from dotenv import load_dotenv

from core.container import Container as CoreContainer
from libs.container import Container as LibsContainer

load_dotenv()


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for the OrangeJuice application.
    """

    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        packages=["app.repos", "app.commits", "app.files"],
    )

    # ==== AppConfig =====

    app_config = providers.Singleton(AppConfig)

    core: CoreContainer = providers.Container(
        CoreContainer,
        config=config,
    )

    libs: LibsContainer = providers.Container(
        LibsContainer,
        config=config,
    )

    core.override(libs)

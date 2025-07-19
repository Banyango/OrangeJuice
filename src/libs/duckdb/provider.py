from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from app.config import AppConfig
from entities.repos.entities import Base


class DuckDbClient:
    def __init__(self, app_config: AppConfig) -> None:
        """
        Initialize the DuckDbClient and connect to the DuckDB database.

        Args:
            app_config (AppConfig): An instance of AppConfig containing the database path.
        """
        logger.info("Initializing orange juice database")

        self.engine = create_engine(f"duckdb:///{app_config.db_path}")

        Base.metadata.create_all(self.engine)

        logger.info("Database initialized successfully.")

    def session(self) -> Session:
        """
        Create a new session for interacting with the DuckDB database.

        Returns:
            Session: A new SQLAlchemy session bound to the DuckDB engine.
        """
        return Session(bind=self.engine)

    def close(self) -> None:
        """
        Close the connection to the DuckDB database.
        """
        self.engine.dispose()

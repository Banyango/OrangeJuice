import os

import duckdb
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from app.config import AppConfig
from core.interfaces.query_client import QueryClient
from entities.repos import Base

class DuckDbClient(QueryClient):
    def __init__(self, app_config: AppConfig) -> None:
        """
        Initialize the DuckDbClient and connect to the DuckDB database.

        Args:
            app_config (AppConfig): An instance of AppConfig containing the database path.
        """
        logger.info("Initializing orange juice database")

        # create file if it does not exist
        if not os.path.exists(app_config.db_path):
            logger.info(f"Creating DuckDB database at {app_config.db_path}")
            directory, filename = os.path.split(app_config.db_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

        self.engine = create_engine(
            f"duckdb:///{app_config.db_path}",
            connect_args={"preload_extensions": ["vss"]},
        )

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

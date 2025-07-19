import duckdb
from fast_depends import Depends
from typing import Optional, Any, List, Tuple, Annotated
from loguru import logger

from app.config import AppConfig


class DuckDbClient:
    def __init__(self, app_config: AppConfig) -> None:
        """
        Initialize the DuckDbClient and connect to the DuckDB database.

        Args:
            app_config (AppConfig): An instance of AppConfig containing the database path.
        """
        self.connection: duckdb.DuckDBPyConnection = duckdb.connect(database=app_config.db_path)

        logger.info("Initializing orange juice database")

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS repos
            (
                id INTEGER NOT NULL,
                path TEXT NOT NULL
            )
            """
        )

        logger.info("Database initialized successfully.")

    def execute(self, query: str, params: Optional[Any] = None) -> List[Tuple]:
        """
        Execute a SQL query against the DuckDB database.

        Args:
            query (str): The SQL query to execute.
            params (Optional[Any]): Optional query parameters.

        Returns:
            List[Tuple]: Query results as a list of tuples.
        """
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            cursor.close()

    def close(self) -> None:
        """
        Close the connection to the DuckDB database.
        """
        self.connection.close()


def duckdb_client_provider(db_path: str = "orangejuice.duckdb") -> DuckDbClient:
    """
    Provides an instance of DuckDbClient.

    Args:
        db_path (str): Path to the DuckDB database file. Defaults to 'orangejuice.duckdb'.

    Returns:
        DuckDbClient: An instance of DuckDbClient.
    """
    client = DuckDbClient(db_path)
    client.initialize()
    return client


DependsOnDuckDbClient = Annotated[DuckDbClient, Depends(duckdb_client_provider)]

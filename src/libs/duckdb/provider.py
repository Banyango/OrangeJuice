import duckdb
from typing import Optional, Any, List, Tuple
from loguru import logger


class DuckDbClient:
    def __init__(self, db_path: str = "orangejuice.db") -> None:
        """
        Initialize the DuckDbClient and connect to the DuckDB database.

        Args:
            db_path (str): Path to the DuckDB database file. Defaults to 'orangejuice.db'.
        """
        self.connection: duckdb.DuckDBPyConnection = duckdb.connect(database=db_path)

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

    def initialize(self):
        logger.info(f"Initializing orange juice database")
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                path TEXT NOT NULL,                
            )
            """
        )
        pass

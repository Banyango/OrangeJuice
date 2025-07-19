from libs.duckdb.provider import DuckDbClient

from dependency_injector.wiring import inject


class AddRepoOperation:
    def __init__(self, duckdb_client: DuckDbClient) -> None:
        """
        Initialize the RepoOperations class.
        This class is responsible for performing operations related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
        """
        self.duckdb_client = duckdb_client

    def execute(self, path: str) -> None:
        self.duckdb_client.execute(
            """
            INSERT INTO repos (id, path) VALUES (?, ?);
            """,
            (1,path),
        )

from typing import Annotated

from dependency_injector.wiring import Provide, inject

from libs.duckdb.provider import DuckDbClient

@inject
class RepoQueries:
    def __init__(self, duckdb_client: DuckDbClient = Provide[DuckDbClient]) -> None:
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.
        """
        self.duckdb_client = duckdb_client

    def get_repos(self) -> list:
        """
        Returns a list of repositories.
        This method executes a query to fetch all repositories from the database.

        Returns:
            list: A list of repositories.
        """
        query = "SELECT * FROM repos"

        return self.duckdb_client.execute(query)
from typing import Annotated

from dependency_injector.wiring import Provide, inject

from libs.duckdb.provider import DuckDbClient
from libs.embeddings.provider import EmbeddingClient


class RepoQueries:
    def __init__(self, duckdb_client: DuckDbClient, embedding_client: EmbeddingClient) -> None:
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
            embedding_client (EmbeddingClient): An instance of EmbeddingClient for handling embeddings.
        """
        self.duckdb_client = duckdb_client
        self.embedding_client = embedding_client

    def query_by_commit_message(self, message: str) -> list:
        """
        Queries repositories by commit message.
        This method executes a query to fetch repositories that contain the specified commit message.

        Args:
            message (str): The commit message to search for.

        Returns:
            list: A list of repositories that match the commit message.
        """
        query = """
        SELECT * FROM repos
        WHERE id IN (
            SELECT repo_id FROM commits
            WHERE message_vector @> ?
        )
        """

        return self.duckdb_client.execute(query, [self.embedding_client.embed_items(message)])


    def get_repos(self) -> list:
        """
        Returns a list of repositories.
        This method executes a query to fetch all repositories from the database.

        Returns:
            list: A list of repositories.
        """
        query = "SELECT * FROM repos"

        return self.duckdb_client.execute(query)

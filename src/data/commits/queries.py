from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient


class CommitQueries:
    def __init__(self, duckdb_client: DuckDbClient, chromadb_client: ChromaClient):
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
            chromadb_client (ChromaClient): An instance of ChromaClient for database operations.
        """
        self.duckdb_client = duckdb_client
        self.chromadb_client = chromadb_client

    def query_by_commit_message(self, message: str, query: str) -> list:
        """
        Queries commit messages.

        Args:
            message (str): The commit message to search for.
            query (str): The query string to search for in the commit messages.

        Returns:
            list: A list of repositories that match the commit message.
        """
        results = self.chromadb_client.query_collection(
            collection_name="commits",
            query=query,
            limit=10,
        )

        return results["documents"]

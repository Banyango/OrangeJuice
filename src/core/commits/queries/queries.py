from core.interfaces.query_client import QueryClient
from core.interfaces.search_client import SearchClient


class CommitQueries:
    def __init__(self, query_client: QueryClient, search_client: SearchClient):
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            query_client (QueryClient): An instance of QueryClient for database operations.
            search_client (SearchClient): An instance of SearchClient for database operations.
        """
        self.query_client = query_client
        self.search_client = search_client

    def query_by_commit_message(self, message: str, query: str) -> list:
        """
        Queries commit messages.

        Args:
            message (str): The commit message to search for.
            query (str): The query string to search for in the commit messages.

        Returns:
            list: A list of repositories that match the commit message.
        """
        results = self.search_client.query_collection(
            collection_name="commits",
            query=query,
            limit=10,
        )

        return results["documents"]

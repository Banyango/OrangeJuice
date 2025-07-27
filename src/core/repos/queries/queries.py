from core.interfaces.query_client import QueryClient
from entities.repos import Repo


class RepoQueries:
    def __init__(self, query_client: QueryClient) -> None:
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            query_client (QueryClient): An instance of QueryClient for database operations.
        """
        self.query_client = query_client

    def get_repos(self) -> list:
        """
        Returns a list of repositories.
        This method executes a query to fetch all repositories from the database.

        Returns:
            list: A list of repositories.
        """
        with self.query_client.session() as session:
            return session.query(Repo).all()

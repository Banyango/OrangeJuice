from entities.repos import Repo
from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient

class RepoQueries:
    def __init__(self, duckdb_client: DuckDbClient, chromadb_client: ChromaClient) -> None:
        """
        Initialize the RepoQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
            chromadb_client (ChromaClient): An instance of ChromaClient for database operations.
        """
        self.duckdb_client = duckdb_client
        self.chromadb_client = chromadb_client

    def get_repos(self) -> list:
        """
        Returns a list of repositories.
        This method executes a query to fetch all repositories from the database.

        Returns:
            list: A list of repositories.
        """
        with self.duckdb_client.session() as session:
            return session.query(Repo).all()

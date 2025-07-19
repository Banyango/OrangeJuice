from entities.repos.entities import Repo
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

    def execute(self, path: str, name: str) -> None:
        with self.duckdb_client.session() as session:
            repo = session.query(Repo).filter(Repo.path == path).one_or_none()

            if repo is not None:
                raise ValueError(f"Repository with path '{path}' already exists.")

            if repo is None:
                repo = Repo(path=path, name=name)
                session.add(repo)
                session.commit()


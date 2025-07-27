from loguru import logger
from tqdm import tqdm

from core.interfaces.query_client import QueryClient
from core.repos.errors import RepoNotFoundError
from core.interfaces.search_client import SearchClient
from entities.commits import Commit
from entities.repos import Repo


class DeleteRepoOperation:
    def __init__(self, query_client: QueryClient, search_client: SearchClient) -> None:
        """
        Initialize the RepoOperations class.
        This class is responsible for performing operations related to repositories.

        Args:
            query_client (QueryClient): An instance of QueryClient for database operations.
            search_client (SearchClient): An instance of SearchClient for handling embeddings.
        """
        self.query_client = query_client
        self.search_client = search_client

    def execute(self, name: str) -> None:
        with self.query_client.session() as session:
            logger.info(f"Deleting repository: {name}")

            repo = session.query(Repo).filter(Repo.name == name).one_or_none()
            if repo is None:
                raise RepoNotFoundError(name)

            commits = session.query(Commit).filter(Commit.repo_id == repo.id).all()
            for commit in tqdm(commits, desc="Deleting commits"):
                session.delete(commit)

            # session.flush is not working as expected, so we use commit directly
            session.commit()

            self.search_client.delete_collection("commits")

            logger.info(f"Deleting repository {name}")
            session.delete(repo)

            session.commit()

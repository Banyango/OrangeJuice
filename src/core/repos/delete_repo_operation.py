from loguru import logger
from tqdm import tqdm

from core.repos.errors import RepoAlreadyExistsError, RepoNotFoundError
from entities.commits import Commit
from entities.repos import Repo
from git import Repo as GitRepo

from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient


class DeleteRepoOperation:
    def __init__(self, duckdb_client: DuckDbClient, chroma_client: ChromaClient) -> None:
        """
        Initialize the RepoOperations class.
        This class is responsible for performing operations related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
            chroma_client (ChromaClient): An instance of ChromaClient for handling embeddings.
        """
        self.duckdb_client = duckdb_client
        self.chromadb_client = chroma_client

    def execute(self, name: str) -> None:
        with self.duckdb_client.session() as session:
            logger.info(f"Deleting repository: {name}")

            repo = session.query(Repo).filter(Repo.name == name).one_or_none()
            if repo is None:
                raise RepoNotFoundError(name)

            commits = session.query(Commit).filter(Commit.repo_id == repo.id).all()
            for commit in tqdm(commits, desc="Deleting commits"):
                session.delete(commit)

            # session.flush is not working as expected, so we use commit directly
            session.commit()

            self.chromadb_client.delete_collection("commits")

            logger.info(f"Deleting repository {name}")
            session.delete(repo)

            session.commit()

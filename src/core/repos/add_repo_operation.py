from tqdm import tqdm

from core.repos.errors import RepoAlreadyExistsError
from entities.commits import Commit
from entities.repos import Repo
from git import Repo as GitRepo

from libs.chromadb.providers import ChromaClient
from libs.duckdb.provider import DuckDbClient


class AddRepoOperation:
    def __init__(
        self, duckdb_client: DuckDbClient, chromadb_client: ChromaClient
    ) -> None:
        """
        Initialize the RepoOperations class.
        This class is responsible for performing operations related to repositories.

        Args:
            duckdb_client (DuckDbClient): An instance of DuckDbClient for database operations.
            chromadb_client (ChromaClient): An instance of ChromaClient for handling embeddings.
        """
        self.chromadb_client = chromadb_client
        self.duckdb_client = duckdb_client

    def execute(self, path: str, name: str) -> None:
        with self.duckdb_client.session() as session:
            repo = session.query(Repo).filter(Repo.path == path).one_or_none()

            if repo is not None:
                raise RepoAlreadyExistsError(path)

            repo = Repo(path=path, name=name)
            session.add(repo)
            session.flush()

            # get all commits in a repo.
            git_repo = GitRepo(path)
            for commit in tqdm(
                git_repo.iter_commits(), desc=f"Adding commits for {name}"
            ):
                print(f"Adding commit {commit.hexsha} for {name}")

                commit_db_object = Commit(
                    commit_hash=commit.hexsha,
                    author=commit.author.name,
                    message=commit.message,
                    date=str(commit.committed_datetime),
                    repo_id=repo.id,
                )

                session.add(commit_db_object)
                session.flush()

                # Embed the commit message
                self.chromadb_client.add_to_collection(
                    collection_name="commits",
                    id=f"rep{repo.id}_com{commit_db_object.id}",
                    data=commit.message,
                    metadata={
                        "repo_id": repo.id,
                        "commit_id": str(commit_db_object.id),
                    },
                )

            session.commit()

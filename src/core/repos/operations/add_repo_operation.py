from tqdm import tqdm

from core.interfaces.query_client import QueryClient
from core.repos.errors import RepoAlreadyExistsError
from core.interfaces.search_client import SearchClient
from entities.commits import Commit
from entities.repos import Repo
from git import Repo as GitRepo

from pathlib import Path


class AddRepoOperation:
    def __init__(self, query_client: QueryClient, search_client: SearchClient) -> None:
        """
        Initialize the RepoOperations class.
        This class is responsible for performing operations related to repositories.

        Args:
            query_client (QueryClient): An instance of QueryClient for database operations.
            search_client (SearchClient): An instance of SearchClient for handling embeddings.
        """
        self.search_client = search_client
        self.query_client = query_client

    def execute(self, path: str, name: str) -> None:
        with self.query_client.session() as session:
            exists = (
                session.query(Repo).filter(Repo.path == path or Repo.name == name).all()
            )
            if exists:
                raise RepoAlreadyExistsError(path)

            repo = Repo(path=str(Path(path).resolve()), name=name)
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
                    repo_id=repo.id,
                )

                session.add(commit_db_object)
                session.flush()

                # Embed the commit message
                self.search_client.add_to_collection(
                    id=f"rep{repo.id}_com{commit_db_object.id}",
                    collection_name="commits",
                    data=commit.message,
                    metadata={
                        "repo_id": repo.id,
                        "commit_id": str(commit_db_object.id),
                    },
                )

            session.commit()

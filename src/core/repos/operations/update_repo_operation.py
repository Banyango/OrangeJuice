from loguru import logger
from git import Repo as GitRepo

from core.interfaces.query_client import QueryClient
from core.repos.errors import RepoNotFoundError
from core.interfaces.search_client import SearchClient

from entities.commits import Commit
from entities.repos import Repo


class UpdateRepoOperation:
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
            repo: Repo | None = (
                session.query(Repo).filter(Repo.name == name).one_or_none()
            )
            if repo is None:
                raise RepoNotFoundError(name)

            matched_commits = []
            commits = session.query(Commit).filter(Commit.repo_id == repo.id).all()
            git_repo = GitRepo(repo.path)

            for new_commit in git_repo.iter_commits():
                existing_commit = (
                    session.query(Commit)
                    .filter(
                        Commit.commit_hash == new_commit.hexsha,
                        Commit.repo_id == repo.id,
                    )
                    .one_or_none()
                )

                if existing_commit is not None:
                    matched_commits.append(existing_commit)

                if existing_commit is None:
                    logger.info(f"Adding new commit {new_commit.hexsha} for {name}")
                    commit_db_object = Commit(
                        commit_hash=new_commit.hexsha,
                        repo_id=repo.id,
                    )
                    session.add(commit_db_object)
                    session.flush()

                    # Embed the commit message
                    self.search_client.add_to_collection(
                        collection_name="commits",
                        data=new_commit.message,
                        id=f"rep{repo.id}_com{commit_db_object.id}",
                        metadata={
                            "repo_id": repo.id,
                            "commit_id": commit_db_object.id,
                            "commit_hash": new_commit.hexsha,
                        },
                    )

            # Remove commits in the db that are not in the matched commits
            matched_commit_hashes = {c.commit_hash for c in matched_commits}
            for db_commit in commits:
                if db_commit.commit_hash not in matched_commit_hashes:
                    logger.info(f"Deleting commit {db_commit.commit_hash} for {name}")
                    session.delete(db_commit)
                    self.search_client.remove_from_collection(
                        collection_name="commits", id=f"rep{repo.id}_com{db_commit.id}"
                    )

            session.commit()

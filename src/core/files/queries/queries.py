from typing import List

from core.interfaces.git_client import GitClient
from core.interfaces.query_client import QueryClient
from entities.repos import Repo

from core.files.queries.models import FileQueryModel


class FilesQueries:
    def __init__(self, git_client: GitClient, query_client: QueryClient) -> None:
        """
        Initialize the FilesQueries class.
        This class is responsible for executing queries related to repositories.

        Args:
            git_client (GitClient): An instance of GitClient for Git operations.
            query_client (QueryClient): An instance of QueryClient for database operations.
        """
        self.git_client = git_client
        self.query_client = query_client

    def get_file_history(self, file_path: str, repo_name: str) -> List[FileQueryModel]:
        """
        Returns the history of a file in the repository.

        Args:
            file_path (str): The path to the file within the repository.
            repo_name (str): The path to the repository.
        """
        with self.query_client.session() as session:
            repo: Repo | None = (
                session.query(Repo).filter(Repo.name == repo_name).one_or_none()
            )

            if not repo:
                return []

            results = []
            for commit in self.git_client.iter_file_history(file_path, repo.path):
                results.append(
                    FileQueryModel(
                        commit_hash=commit.hexsha,
                        message=commit.message.strip(),
                        author=commit.author.name,
                        date=commit.committed_datetime.isoformat(),
                    )
                )

            return list(results)

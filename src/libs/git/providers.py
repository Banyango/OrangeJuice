from typing import Iterator

from git import Repo, Commit

from core.interfaces.git_client import GitClient


class PythonGitClient(GitClient):
    def iter_file_history(self, file_name: str, repo_path: str) -> Iterator[Commit]:
        """
        Retrieve the history of a file in the repository.

        Args:
            file_name (str): The name of the repository.
            repo_path (str): The path to the file within the repository.

        Returns:
            Dict: A dictionary containing the file history.
        """
        git_repo = Repo(repo_path)

        return git_repo.iter_commits(paths=file_name)

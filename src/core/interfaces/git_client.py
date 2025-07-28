from abc import ABC, abstractmethod
from typing import Iterator

from git import Commit


class GitClient(ABC):
    @abstractmethod
    def iter_file_history(self, file_name: str, repo_path: str) -> Iterator[Commit]:
        """
        Retrieve the history of a file in the repository.

        Args:
            file_name (str): The path to the file relative to the repository root.
            repo_path (str): The path to the repository.
        """
        pass

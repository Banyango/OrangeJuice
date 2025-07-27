from abc import ABC, abstractmethod
from typing import Dict, Iterator

from git import Commit


class GitClient(ABC):
    @abstractmethod
    def file_history(self, name: str, repo_path: str) -> Iterator[Commit]:
        """
        Retrieve the history of a file in the repository.

        Args:
            name (str): The name of the repository.
            repo_path (str): The path to the file within the repository.
        """
        pass

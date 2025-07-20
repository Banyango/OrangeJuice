class RepoAlreadyExistsError(Exception):
    """Raised when trying to create a repository that already exists."""

    def __init__(self, path: str):
        super().__init__(f"Repository with path ='{path}' already exists.")


class RepoNotFoundError(Exception):
    """Raised when a repository is not found."""

    def __init__(self, name: str):
        super().__init__(f"Repository with name '{name}' not found.")

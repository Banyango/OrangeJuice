class RepoAlreadyExistsError(Exception):
    """Raised when trying to create a repository that already exists."""
    def __init__(self, path: str):
        super().__init__(f"Repository with path ='{path}' already exists.")
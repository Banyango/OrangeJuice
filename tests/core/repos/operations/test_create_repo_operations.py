from unittest.mock import MagicMock, patch
import pytest
from core.repos.operations.add_repo_operation import AddRepoOperation
from core.repos.errors import RepoAlreadyExistsError
from entities.repos import Repo


def test_execute_should_raise_repo_already_exists_error_when_name_exists():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    session.query.return_value.filter.return_value.all.return_value = [
        Repo(name="existing-repo", path="/path/to/repo")
    ]
    client.session.return_value.__enter__.return_value = session

    # Act & Assert
    with patch("core.repos.operations.add_repo_operation.GitRepo", MagicMock()):
        op = AddRepoOperation(query_client=client, search_client=MagicMock())
        with pytest.raises(RepoAlreadyExistsError):
            op.execute("/path/to/repo", "existing-repo")


def test_execute_should_add_repo():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    session.query.return_value.filter.return_value.all.return_value = []
    client.session.return_value.__enter__.return_value = session
    search_client = MagicMock()

    with patch("core.repos.operations.add_repo_operation.GitRepo", MagicMock()):
        # Act
        op = AddRepoOperation(query_client=client, search_client=search_client)
        op.execute("/new/path/to/repo", "new-repo")

    # Assert
    session.add.assert_called()
    session.flush.assert_called_once()

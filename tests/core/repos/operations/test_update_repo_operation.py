from unittest.mock import MagicMock, patch
import pytest
from core.repos.operations.update_repo_operation import UpdateRepoOperation
from core.repos.errors import RepoNotFoundError
from entities.repos import Repo

def test_execute_should_raise_repo_not_found_error():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    session.query.return_value.filter.return_value.one_or_none.return_value = None
    client.session.return_value.__enter__.return_value = session

    with patch("core.repos.operations.update_repo_operation.GitRepo", MagicMock()):
        op = UpdateRepoOperation(query_client=client, search_client=MagicMock())
        with pytest.raises(RepoNotFoundError):
            op.execute("nonexistent-repo")

def test_execute_should_update_repo():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    repo = Repo(name="test-repo", path="/old/path/to/repo")
    session.query.return_value.filter.return_value.one_or_none.return_value = repo
    session.query.return_value.filter.return_value.all.return_value = []  # No existing commits
    client.session.return_value.__enter__.return_value = session
    search_client = MagicMock()

    # Mock GitRepo and its iter_commits
    mock_git_repo = MagicMock()
    mock_git_repo.iter_commits.return_value = [MagicMock(hexsha="abc123"), MagicMock(hexsha="def456")]
    with patch("core.repos.operations.update_repo_operation.GitRepo", return_value=mock_git_repo):
        op = UpdateRepoOperation(query_client=client, search_client=search_client)
        op.execute("test-repo")

    # Assert
    session.commit.assert_called()
    mock_git_repo.iter_commits.assert_called_once()
    assert repo.name == "test-repo"
    assert repo.path == "/old/path/to/repo"


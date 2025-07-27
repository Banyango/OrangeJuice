from unittest.mock import MagicMock

import pytest
from core.repos.delete_repo_operation import DeleteRepoOperation
from core.repos.errors import RepoNotFoundError
from entities.commits import Commit
from entities.repos import Repo


def test_execute_should_raise_repo_not_found_error():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    session.query.return_value.filter.return_value.one_or_none.return_value = None
    client.session.return_value.__enter__.return_value = session

    # Act & Assert
    op = DeleteRepoOperation(query_client=client, chroma_client=MagicMock())
    with pytest.raises(RepoNotFoundError):
        op.execute("nonexistent-repo")


def test_execute_should_delete_repo():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    repo = Repo(name="test-repo", path="/path/to/repo")
    session.query.return_value.filter.return_value.one_or_none.return_value = repo
    client.session.return_value.__enter__.return_value = session

    # Act
    op = DeleteRepoOperation(query_client=client, chroma_client=MagicMock())
    op.execute("test-repo")

    # Assert
    session.query.assert_called_with(Commit)
    session.query.return_value.filter.assert_called()
    session.delete.assert_called_once_with(repo)
    assert session.commit.call_count == 2

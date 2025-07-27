from unittest.mock import MagicMock, patch
import pytest
from core.repos.operations.update_repo_operation import UpdateRepoOperation
from core.repos.errors import RepoNotFoundError
from entities.commits import Commit
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


def test_execute_should_not_add_commits_when_commits_exist_in_db():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    repo = Repo(name="test-repo", path="/old/path/to/repo")
    commit1 = Commit(id=1, commit_hash="abc123", repo_id=repo.id)
    commit2 = Commit(id=2, commit_hash="def456", repo_id=repo.id)
    session.query.return_value.filter.return_value.one_or_none.side_effect = [
        repo,
        commit1,
        commit2,
    ]
    session.query.return_value.filter.return_value.all.return_value = [
        commit1,
        commit2,
    ]  # No existing commits
    client.session.return_value.__enter__.return_value = session
    search_client = MagicMock()

    # Mock GitRepo and its iter_commits
    mock_git_repo = MagicMock()
    mock_git_repo.iter_commits.return_value = [
        MagicMock(hexsha="abc123"),
        MagicMock(hexsha="def456"),
    ]
    with patch(
        "core.repos.operations.update_repo_operation.GitRepo",
        return_value=mock_git_repo,
    ):
        op = UpdateRepoOperation(query_client=client, search_client=search_client)
        op.execute("test-repo")

    # Assert
    session.commit.assert_called()
    session.add.assert_not_called()
    mock_git_repo.iter_commits.assert_called_once()
    search_client.add_to_collection.assert_not_called()


def test_execute_should_add_commits_when_commits_do_not_exist_in_db():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    repo = Repo(id=1,name="test-repo", path="/old/path/to/repo")
    commit1 = Commit(id=1, commit_hash="abc123", repo_id=repo.id)
    session.query.return_value.filter.return_value.one_or_none.side_effect = [
        repo,
        commit1,
        None,
    ]
    session.query.return_value.filter.return_value.all.return_value = []  # No existing commits
    client.session.return_value.__enter__.return_value = session
    search_client = MagicMock()

    def mock_assign_id_that_flush_would_assign(commit):
        commit.id = "1"  # Simulate ID assignment
        return commit

    session.add.side_effect = mock_assign_id_that_flush_would_assign

    # Mock GitRepo and its iter_commits
    mock_git_repo = MagicMock()
    mock_git_repo.iter_commits.return_value = [
        MagicMock(hexsha="abc123"),
        MagicMock(hexsha="def456", message="New commit message")
    ]
    with patch(
        "core.repos.operations.update_repo_operation.GitRepo",
        return_value=mock_git_repo,
    ):
        op = UpdateRepoOperation(query_client=client, search_client=search_client)
        op.execute("test-repo")

     # Assert
    session.commit.assert_called()
    session.add.assert_called()
    mock_git_repo.iter_commits.assert_called_once()
    search_client.add_to_collection.assert_called_with(
        collection_name="commits",
        data="New commit message",
        id=f"rep1_com1",
        metadata={
            "repo_id": repo.id,
            "commit_id": "1",
            "commit_hash": "def456"
        },
    )


def test_execute_should_delete_commits_when_commits_do_not_exist_in_current_git_repo():
    # Arrange
    client = MagicMock()
    session = MagicMock()
    repo = Repo(name="test-repo", path="/old/path/to/repo")
    commit1 = Commit(id=1, commit_hash="abc123", repo_id=repo.id)
    commit2 = Commit(id=1, commit_hash="def123", repo_id=repo.id)
    session.query.return_value.filter.return_value.one_or_none.side_effect = [
        repo,
        commit1,
        commit2,
    ]
    session.query.return_value.filter.return_value.all.return_value = [commit1, commit2]
    client.session.return_value.__enter__.return_value = session
    search_client = MagicMock()

    # Mock GitRepo and its iter_commits
    mock_git_repo = MagicMock()
    mock_git_repo.iter_commits.return_value = [
        MagicMock(hexsha="abc123"),
    ]
    with patch(
        "core.repos.operations.update_repo_operation.GitRepo",
        return_value=mock_git_repo,
    ):
        op = UpdateRepoOperation(query_client=client, search_client=search_client)
        op.execute("test-repo")

    # Assert
    session.commit.assert_called()
    session.delete.assert_called_with(commit2)
    mock_git_repo.iter_commits.assert_called_once()
    search_client.remove_from_collection.assert_called_with(
        collection_name="commits", id=f"rep{repo.id}_com{commit2.id}"
    )

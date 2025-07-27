from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence

from entities.base import Base
from libs.chromadb.base import CollectionBase

from libs.chromadb.providers import collection


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, Sequence("commit_id_sequence"), primary_key=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    commit_hash = Column(String, nullable=False)


@collection
class CommitCollection(CollectionBase):
    name = "commits"
    metadata = {
        "sha": "the SHA of the commit",
        "repo_id": "the ID of the repository",
        "commit_id": "the ID of the commit",
    }

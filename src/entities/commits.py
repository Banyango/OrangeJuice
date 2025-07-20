from chromadb.types import Collection
from sqlalchemy import Integer, String, Float, ARRAY, Index
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence

from entities.base import Base

from libs.chromadb.providers import collection


class Commit(Base):
    __tablename__ = 'commits'

    id = Column(Integer, Sequence("repo_id_sequence"), primary_key=True)
    repo_id = Column(Integer, ForeignKey('repos.id'))
    commit_hash = Column(String, nullable=False)
    author = Column(String, nullable=False)
    message = Column(String, nullable=False)
    date = Column(String, nullable=False)
    message_vector = Column(ARRAY(Float), nullable=True)


@collection
class CommitCollection:
    name = "commits"
    metadata = {
        "description": "Collection of commits",
        "created_at": datetime.datetime.now().isoformat(),
    }

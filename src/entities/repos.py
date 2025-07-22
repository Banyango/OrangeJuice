from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from entities.base import Base


class Repo(Base):
    __tablename__ = "repos"
    id = Column(Integer, Sequence("repo_id_sequence"), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    path = Column(String, nullable=False, unique=True)
    commits = relationship("Commit", backref="repo")

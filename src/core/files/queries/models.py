from dataclasses import dataclass


@dataclass
class FileQueryModel:
    commit_hash: str
    message: str
    author: str
    date: str

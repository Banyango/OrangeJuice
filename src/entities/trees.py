from libs.chromadb.base import CollectionBase
from libs.chromadb.providers import collection


@collection
class TreesCollection(CollectionBase):
    name = "trees"
    metadata = {
        "sha": "the SHA of the commit",
        "repo_id": "the ID of the repository",
        "commit_id": "the ID of the commit",
    }
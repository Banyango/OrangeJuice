from abc import ABC, abstractmethod
from typing import Dict


class SearchClient(ABC):
    @abstractmethod
    def create_collection(self, name):
        """
        Create a new collection with the given name.
        Args:
            name (str): The name of the collection to create.
        """
        pass

    @abstractmethod
    def add_to_collection(
        self, collection_name: str, data: str, id: str, metadata: Dict[str, str]
    ):
        """
        Add data to a specified collection.
        Args:
            collection_name (str): The name of the collection.
            data (str): The data to add.
            id (str): The unique identifier for the data.
            metadata (Dict[str, str]): Metadata associated with the data.
        """
        pass

    @abstractmethod
    def delete_collection(self, name: str):
        """
        Delete a collection by name.
        Args:
            name (str): The name of the collection to delete.
        """
        pass

    @abstractmethod
    def query_collection(self, collection_name: str, query: str, limit: int = 10):
        """
        Query a collection for data matching the query string.
        Args:
            collection_name (str): The name of the collection to query.
            query (str): The query string.
            limit (int, optional): Maximum number of results to return. Defaults to 10.
        """
        pass

    @abstractmethod
    def remove_from_collection(self, collection_name: str, id: str):
        """
        Remove an item from a collection by its ID.
        Args:
            collection_name (str): The name of the collection.
            id (str): The unique identifier of the item to remove.
        """
        pass

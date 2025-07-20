import chromadb
from typing import Type, Dict

from chromadb import Settings

from app.embeddings.embedding_function import CustomEmbeddingFunction
from app.config import AppConfig
from .base import CollectionBase

chroma_collections_registry: list[Type[CollectionBase]] = []


def collection(cls: Type[CollectionBase]) -> Type[CollectionBase]:
    """
    Register a class as a Chroma collection.

    Args:
        cls: The class to register
    """
    # Ensure the name attribute is present
    if not hasattr(cls, "name"):
        raise ValueError(f"Class {cls.__name__} must have a 'name' attribute.")

    # Ensure the metadata attribute is present
    if not hasattr(cls, "metadata"):
        raise ValueError(f"Class {cls.__name__} must have a 'metadata' attribute.")

    # Ensure the class is not already registered
    if cls in chroma_collections_registry:
        raise ValueError(
            f"Class {cls.__name__} is already registered as a Chroma collection."
        )

    chroma_collections_registry.append(cls)

    return cls


class ChromaClient:
    def __init__(
        self, app_config: AppConfig, embedding_function: CustomEmbeddingFunction
    ):
        """
        Initializes the ChromaClient with a given client.

        Args:
            app_config (AppConfig): An instance of AppConfig containing configuration settings.
            embedding_function (CustomEmbeddingFunction): An instance of CustomEmbeddingFunction for handling embeddings.
        """
        self.client = chromadb.Client(
            settings=Settings(persist_directory=app_config.chroma_persist_directory)
        )

        for c in chroma_collections_registry:
            self.client.create_collection(
                c.name, metadata=c.metadata, embedding_function=embedding_function
            )

    def create_collection(self, name):
        """
        Creates a collection in the Chroma database.

        Args:
            name (str): The name of the collection to create.

        Returns:
            Collection: The created collection.
        """
        return self.client.create_collection(name)

    def add_to_collection(
        self, collection_name: str, data: str, id: str, metadata: Dict[str, str]
    ):
        """
        Adds data to a specified collection in the Chroma database.

        Args:
            collection_name (str): The name of the collection to add data to.
            data (str): The data to be added.
            id (str): The unique identifier for the data.
            metadata (Dict[str, str]): Metadata associated with the data.
        """
        self.client.get_collection(collection_name).add(
            ids=[id],
            documents=[data],
            metadatas=[metadata],
        )

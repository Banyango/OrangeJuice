from typing import Any

from chromadb import Embeddings, Documents, EmbeddingFunction

from app.config import AppConfig
from libs.embeddings.provider import EmbeddingClient

class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, app_config: AppConfig, embedding_client: EmbeddingClient) -> None:
        """
        Initialize the embedding function with a client.

        Args:
            app_config (AppConfig): An instance of AppConfig containing configuration settings.
            embedding_client (EmbeddingClient): An instance of EmbeddingClient for handling embeddings.
        """
        super().__init__()
        self.app_config: AppConfig = app_config
        self.embedding_client: EmbeddingClient = embedding_client

    def __call__(self, documents: Documents) -> Embeddings:
        """
        Generate embeddings for the given input documents.

        Args:
            documents (Documents): The input documents to embed.
        """
        if not isinstance(documents, Documents):
            raise ValueError("Input must be of type 'Documents'.")

        # Extract text from the input documents
        text_items = [doc for doc in documents]
        if not text_items:
            raise ValueError("Input documents must contain text.")

        # Generate embeddings using the embedding client
        tensor_list = self.embedding_client.embed_items(text_items)

        # Convert list of tensors to Embeddings object
        embeddings = Embeddings(tensor_list)

        return embeddings
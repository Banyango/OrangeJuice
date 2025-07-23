from typing import Optional, List

import torch
from loguru import logger
from sentence_transformers import SentenceTransformer
from torch import Tensor

from app.config import AppConfig


class EmbeddingClient:
    def __init__(self, app_config: AppConfig):
        """
        Initialize the embedding provider with a name.

        Args:
            app_config (AppConfig): An instance of AppConfig containing configuration settings.
        """
        self.model: str = app_config.embedding_model
        self.embedding_model: Optional[SentenceTransformer] = None

    def embed_items(self, text_items: List[str] | str) -> List[Tensor] | Tensor:
        """
        Generate an embedding for the given text.

        Args:
            text_items (str): The text to embed.
        """
        if self.embedding_model is None:
            self.load_model()

        embeddings = self.embedding_model.encode(
            text_items,
            show_progress_bar=False,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        return embeddings

    def load_model(self):
        logger.info(f"Loading embedding model: {self.model}")
        self.embedding_model = SentenceTransformer(
            self.model,
            tokenizer_kwargs={"padding_side": "left"},
            device="cuda" if torch.cuda.is_available() else "cpu",
        )

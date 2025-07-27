from dataclasses import dataclass
import os


@dataclass
class AppConfig:
    def __init__(self):
        """
        Initialize the application configuration.
        This class holds the configuration settings for the application.
        """
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", ".chroma")
        self.embedding_model = "Qwen/Qwen3-Embedding-0.6B"
        self.db_path = os.getenv("DUCKDB_LOCATION", "orangejuice.duckdb")

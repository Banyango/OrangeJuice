from dataclasses import dataclass
import os


@dataclass
class AppConfig:
    def __init__(self):
        """
        Initialize the application configuration.
        This class holds the configuration settings for the application.
        """
        self.db_path = os.getenv("DUCKDB_LOCATION", "orangejuice.duckdb")

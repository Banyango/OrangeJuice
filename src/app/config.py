from dataclasses import dataclass


@dataclass
class AppConfig:
    DUCKDB_CONNECTION_STRING: str = "duckdb:///:memory:"

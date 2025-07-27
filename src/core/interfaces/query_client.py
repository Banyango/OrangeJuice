from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class QueryClient(ABC):
    @abstractmethod
    def session(self) -> Session:
        """
        Create and return a new database session.

        Returns:
            Session: A new SQLAlchemy session for database operations.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the database connection or session.
        """
        pass

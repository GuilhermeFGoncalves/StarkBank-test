from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence


class Database(ABC):
    """Generic interface a concrete DB backend (SQLite, Postgres, MySQL, ...) must implement."""

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def execute(self, query: str, params: Sequence[Any] = ()) -> None:
        ...

    @abstractmethod
    def fetch_one(self, query: str, params: Sequence[Any] = ()) -> Optional[tuple]:
        ...

    @abstractmethod
    def fetch_all(self, query: str, params: Sequence[Any] = ()) -> list:
        ...

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

import sqlite3
from typing import Any, Optional, Sequence

from database.base import Database


class SQLiteDatabase(Database):
    def __init__(self, path: str):
        self.path = path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.path)

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute(self, query: str, params: Sequence[Any] = ()) -> None:
        self.connection.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query: str, params: Sequence[Any] = ()) -> Optional[tuple]:
        return self.connection.execute(query, params).fetchone()

    def fetch_all(self, query: str, params: Sequence[Any] = ()) -> list:
        return self.connection.execute(query, params).fetchall()

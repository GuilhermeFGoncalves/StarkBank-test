from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from database.base import Database

DB_PATH = "invoice_log.sqlite3"


@dataclass
class InvoiceLog:
    invoice_id: str
    status: str
    updated_at: str


class InvoiceLogRepository:
    def __init__(self, db: Database):
        self.db = db
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS invoice_log (
                invoice_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

    def register_sent(self, invoice_id: str) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO invoice_log (invoice_id, status, updated_at) VALUES (?, ?, ?)",
            (invoice_id, "send", datetime.now(timezone.utc).isoformat()),
        )

    def update_status(self, invoice_id: str, status: str) -> None:
        self.db.execute(
            "UPDATE invoice_log SET status = ?, updated_at = ? WHERE invoice_id = ?",
            (status, datetime.now(timezone.utc).isoformat(), invoice_id),
        )

    def get(self, invoice_id: str) -> Optional[InvoiceLog]:
        row = self.db.fetch_one(
            "SELECT invoice_id, status, updated_at FROM invoice_log WHERE invoice_id = ?",
            (invoice_id,),
        )
        if row is None:
            return None
        return InvoiceLog(invoice_id=row[0], status=row[1], updated_at=row[2])

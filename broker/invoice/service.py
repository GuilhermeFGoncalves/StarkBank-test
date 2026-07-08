
import logging
from builtins import staticmethod, str
import starkbank
from starkbank.error import InputErrors, StarkError
# from ..dto import InvoicePayload
from broker.project import get_project
from database.sqlite import SQLiteDatabase
from broker.invoice.models import DB_PATH, InvoiceLogRepository

logger = logging.getLogger(__name__)

class InvoiceService:
    @staticmethod
    def send_invoice(invoices):
        try:
            created_invoices = starkbank.invoice.create(invoices, get_project())
        except InputErrors as exc:
            logger.error(
                "Stark Bank rejected the invoice batch: %s",
                [f"{error.code}: {error.message}" for error in exc.errors],
            )
            raise
        except StarkError as exc:
            logger.error("Failed to create invoices on Stark Bank: %s", exc)
            raise

        try:
            with SQLiteDatabase(DB_PATH) as db:
                repository = InvoiceLogRepository(db)
                for invoice in created_invoices:
                    repository.register_sent(invoice.id)
        except Exception:
            logger.exception(
                "Invoices %s were created on Stark Bank but failed to be logged locally",
                [invoice.id for invoice in created_invoices],
            )
            raise

        return created_invoices

    @staticmethod
    def calculate_net_amount(invoice) -> int:
        """Amount actually credited to our balance when the invoice settles.

        invoice.amount is Stark Bank's final settled value: nominal_amount already
        adjusted by fine_amount/interest_amount (late payment) and net of
        discount_amount (early payment) - so those three aren't subtracted again
        here. What's still charged on top:
        - invoice.fee: Stark Bank's own service fee for the invoice
        - invoice.splits: amounts routed straight to other receivers, which never
          land in our balance in the first place
        """
        split_amount = sum(split.get("amount", 0) for split in invoice.splits)
        return invoice.amount - (invoice.fee or 0) - split_amount

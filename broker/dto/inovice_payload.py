
from builtins import int, str
from dataclasses import dataclass

@dataclass
class InvoicePayload:
    amount: int
    name: str
    tax_id: str
from dataclasses import dataclass, field
from typing import List


@dataclass
class InvoiceDescription:
    key: str
    value: str

    @staticmethod
    def from_dict(data: dict) -> "InvoiceDescription":
        return InvoiceDescription(
            key=data.get("key"),
            value=data.get("value"),
        )


@dataclass
class InvoiceDiscount:
    due: str
    percentage: float

    @staticmethod
    def from_dict(data: dict) -> "InvoiceDiscount":
        return InvoiceDiscount(
            due=data.get("due"),
            percentage=data.get("percentage"),
        )


@dataclass
class Invoice:
    amount: int
    brcode: str
    created: str
    due: str
    expiration: int
    fee: int
    fine: float
    fine_amount: int
    id: str
    interest: float
    interest_amount: int
    link: str
    name: str
    nominal_amount: int
    pdf: str
    status: str
    tax_id: str
    updated: str
    discount_amount: int = 0
    descriptions: List[InvoiceDescription] = field(default_factory=list)
    discounts: List[InvoiceDiscount] = field(default_factory=list)
    rules: List[dict] = field(default_factory=list)
    splits: List[dict] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    transaction_ids: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "Invoice":
        return Invoice(
            amount=data.get("amount"),
            brcode=data.get("brcode"),
            created=data.get("created"),
            discount_amount=data.get("discountAmount"),
            descriptions=[InvoiceDescription.from_dict(d) for d in data.get("descriptions", [])],
            discounts=[InvoiceDiscount.from_dict(d) for d in data.get("discounts", [])],
            due=data.get("due"),
            expiration=data.get("expiration"),
            fee=data.get("fee"),
            fine=data.get("fine"),
            fine_amount=data.get("fineAmount"),
            id=data.get("id"),
            interest=data.get("interest"),
            interest_amount=data.get("interestAmount"),
            link=data.get("link"),
            name=data.get("name"),
            nominal_amount=data.get("nominalAmount"),
            pdf=data.get("pdf"),
            rules=data.get("rules", []),
            splits=data.get("splits", []),
            status=data.get("status"),
            tags=data.get("tags", []),
            tax_id=data.get("taxId"),
            transaction_ids=data.get("transactionIds", []),
            updated=data.get("updated"),
        )


@dataclass
class Log:
    created: str
    id: str
    invoice: Invoice
    type: str
    errors: List[dict] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "Log":
        return Log(
            created=data.get("created"),
            errors=data.get("errors", []),
            id=data.get("id"),
            invoice=Invoice.from_dict(data.get("invoice", {})),
            type=data.get("type"),
        )


@dataclass
class Event:
    created: str
    id: str
    log: Log
    subscription: str
    workspace_id: str

    @staticmethod
    def from_dict(data: dict) -> "Event":
        return Event(
            created=data.get("created"),
            id=data.get("id"),
            log=Log.from_dict(data.get("log", {})),
            subscription=data.get("subscription"),
            workspace_id=data.get("workspaceId"),
        )


@dataclass
class EventPayload:
    event: Event

    @staticmethod
    def from_dict(data: dict) -> "EventPayload":
        return EventPayload(event=Event.from_dict(data.get("event", {})))

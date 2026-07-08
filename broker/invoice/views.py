import json
import starkbank
from starkbank.error import InvalidSignatureError
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from broker.dto.event_payload import EventPayload
from broker.project import get_project
from database.sqlite import SQLiteDatabase
from broker.invoice.models import DB_PATH, InvoiceLogRepository
from broker.invoice.service import InvoiceService

STARK_BANK_RECEIVER = {
    "bank_code": settings.STARKBANK_RECEIVER_BANK_CODE,
    "branch_code": settings.STARKBANK_RECEIVER_BRANCH_CODE,
    "account_number": settings.STARKBANK_RECEIVER_ACCOUNT_NUMBER,
    "account_type": settings.STARKBANK_RECEIVER_ACCOUNT_TYPE,
    "tax_id": settings.STARKBANK_RECEIVER_TAX_ID,
    "name": settings.STARKBANK_RECEIVER_NAME,
}

@csrf_exempt
@require_POST
def listen_invoice(request):
    content = request.body.decode("utf-8")
    signature = request.headers.get("Digital-Signature")

    if not signature:
        return HttpResponseBadRequest("Missing Digital-Signature header")

    project = get_project()

    try:
        starkbank.event.parse(
            content=content,
            signature=signature,
            user=project,
        )
    except InvalidSignatureError:
        return HttpResponseBadRequest("Invalid signature")

    payload = EventPayload.from_dict(json.loads(content))
    event = payload.event

    if event.subscription == "invoice" and event.log.type == "credited":
        invoice = event.log.invoice

        with SQLiteDatabase(DB_PATH) as db:
            repository = InvoiceLogRepository(db)
            log = repository.get(invoice.id)

            if log is None:
                return HttpResponseBadRequest("Invoice not tracked")

            if log.status == "credited":
                return HttpResponse(status=200)

            starkbank.transfer.create([
                starkbank.Transfer(
                    amount=InvoiceService.calculate_net_amount(invoice),
                    tags=[f"invoice/{invoice.id}"],
                    **STARK_BANK_RECEIVER,
                ),
            ], user=project)

            repository.update_status(invoice.id, "credited")

        return HttpResponse(status=200)

    return HttpResponseBadRequest("Invalid event")
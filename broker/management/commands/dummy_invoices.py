import random
from django.core.management.base import BaseCommand
from broker.invoice.service import InvoiceService
import starkbank

class Command(BaseCommand):

    def handle(self, *args, **options):
        count = random.randint(8, 12)
        service = InvoiceService()
        invoices =[]

        for _ in range(count):
            invoices.append(starkbank.Invoice(
                amount = 10000,
                name = "Guilherme",
                tax_id = "52023807808",
            ))

        service.send_invoice(invoices)
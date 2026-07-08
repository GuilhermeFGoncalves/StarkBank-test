from celery import shared_task
from django.core.management import call_command


@shared_task
def send_dummy_invoices():
    call_command("dummy_invoices")

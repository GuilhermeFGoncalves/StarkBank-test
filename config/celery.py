import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-dummy-invoices-every-24h": {
        "task": "broker.tasks.send_dummy_invoices",
        "schedule": 60 * 60 * 24,
    },
}

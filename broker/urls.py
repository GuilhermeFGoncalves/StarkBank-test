from django.urls import path

from broker.invoice import views

urlpatterns = [
    path("stark/", views.listen_invoice, name="listen_invoice"),
]

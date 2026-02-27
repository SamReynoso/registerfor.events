
from django.urls import path
from invoice import views


app_name = 'invoice'

urlpatterns = [
    path('invoices/',
         views.invoices,
         name='invoices'),

    path("invoices/<int:invoice_id>/",
         views.invoice,
         name="invoice"),

    path("invoices/<int:invoice_id>/view/",
         views.view_pdf,
         name="view_pdf"),

    path("invoices/<int:invoice_id>/download/",
         views.download_pdf,
         name="download_invoice_pdf"),
]

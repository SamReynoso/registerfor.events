
from django.urls import path
from invoice import views


app_name = 'invoice'

urlpatterns = [
    path('',
         views.records,
         name='records'),

    path('invoices/',
         views.invoices,
         name='invoices'),

    path("invoices/<int:invoice_id>/",
         views.invoice_details,
         name="invoice_details"),

    path("invoices/<int:invoice_id>/view/",
         views.view_invoice,
         name="view_invoice_pdf"),

    path("invoices/<int:invoice_id>/download/",
         views.download_invoice,
         name="download_invoice_pdf"),
]

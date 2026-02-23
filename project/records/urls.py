
from django.urls import path
from records import views


app_name = 'records'

urlpatterns = [
    path('',
         views.records,
         name='records'),

    path('registrations/',
         views.records_registrations,
         name='records_registrations'),

    path('registrations/<int:registration_id>',
         views.registration_details,
         name='registration_details'),


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

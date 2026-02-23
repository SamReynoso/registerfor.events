
from django.urls import path
from records import views


app_name = 'records'

urlpatterns = [
    path('test/',
         views.test,
         name='test'),

    path("invoices/<int:invoice_id>/view/",
         views.view_invoice,
         name="view_pdf"),

    path("invoices/<int:invoice_id>/download/",
         views.download_invoice,
         name="download_invoice"),
]

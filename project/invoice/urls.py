
from django.urls import path
from invoice import views


app_name = 'invoice'

urlpatterns = [

    path('created/',
         views.created,
         name='created'),

    path('events/',
         views.events,
         name='events'),

    path('events/<int:event_id>/',
         views.event_invoices,
         name='event_invoices'),


    path('create/<int:registration_id>/',
         views.create,
         name='create'),


    path('create/<int:registration_id>/all/',
         views.create_all,
         name='create_all'),


    path('issue/<int:invoice_id>',
         views.received,
         name='received'),


    path('issue/event/<int:event_id>',
         views.issue_event,
         name='issue_event'),


    path('received/',
         views.received,
         name='received'),


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

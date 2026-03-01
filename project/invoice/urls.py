
from django.urls import path
from invoice import views, post


app_name = 'invoice'

urlpatterns = [

    path('created/',
         views.created,
         name='created'),

    path('events/',
         views.events,
         name='events'),

    path('event/<int:event_id>/',
         views.event_invoices,
         name='event_invoices'),


    path('issue/<int:invoice_id>',
         views.received,
         name='received'),


    path('issue/event/<int:event_id>',
         views.issue_event,
         name='issue_event'),


    path('received/',
         views.received,
         name='received'),


    path('<int:invoice_id>/preview/',
         views.preview,
         name='preview'),

    path('<int:invoice_id>/view/',
         views.view_pdf,
         name='view_pdf'),

    path('<int:invoice_id>/download/',
         views.download_pdf,
         name='download_invoice_pdf'),
] + [
    path('<int:invoice_id>/status/issue/',
         post.status_issue,
         name='status_issue'),

    path('<int:invoice_id>/status/sent/',
         post.status_sent,
         name='status_sent'),

    path('<int:invoice_id>/status/paid/',
         post.status_paid,
         name='status_paid'),

    path('<int:invoice_id>/status/rest/',
         post.reset,
         name='reset'),

    path('<int:invoice_id>/error/past-due/',
         post.error_past_due,
         name='error_past_due'),

    path('<int:invoice_id>/error/void-due/',
         post.error_void,
         name='error_void'),

    path('<int:invoice_id>/error/refund/',
         post.error_refund,
         name='error_refund'),

    path('<int:invoice_id>/error/modified/clear',
         post.clear_modified,
         name='clear_modified'),

    path('<int:invoice_id>/error/past-due/clear',
         post.clear_past_due,
         name='clear_past_due'),

    path('<int:invoice_id>/error/void/clear',
         post.clear_void,
         name='clear_void'),

    path('<int:invoice_id>/error/refund/clear',
         post.clear_refund,
         name='clear_refund'),

        ]



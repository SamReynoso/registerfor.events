from django.urls import path
from host import views
from host import post


app_name = 'host'

urlpatterns = [
    path('',
         views.hosting,
         name='hosting'),

    path('event/<int:event_id>',
         views.event,
         name='event'),


    path('event/<int:event_id>/rsvps/',
         views.invitations,
         name='invitations'),

    path('event/<int:event_id>/invite/',
         views.invite,
         name='invite'),

    path('event/registration/<int:registration_id>/',
         views.registration,
         name='registration'),

    path('event/registration/item/<int:registration_item_id>/',
         views.registration_item,
         name='registration_item'),

    path('event/division/<int:division_id>/',
         views.division,
         name='division'),

    path('event/<int:event_id>/embed/',
         views.embed,
         name='embed'),



] + [
    path('event/create/',
         post.event_create,
         name='event_create'),
    path('event/<int:event_id>/update/',
         post.event_update,
         name='event_update'),
    path('event/<int:event_id>/delete',
         post.event_delete,
         name='event_delete'),
    path('event/<int:event_id>/poster/update/',
         post.event_poster_update,
         name='event_poster_update'),
    path('event/<int:event_id>/poster/delete/',
         post.event_poster_delete,
         name='event_poster_delete'),
    path('event-divisions/<int:event_id>/',
         post.event_divisions,
         name='event_divisions'),
    path('event/registration/<int:registration_id>/cancel',
         post.registration_cancel,
         name='registration_cancel'),


    path('event/<int:event_id>/status/open/',
         post.status_open,
         name='status_open'),

    path('event/<int:event_id>/status/close',
         post.status_close,
         name='status_close'),

    path('event/<int:event_id>/status/scheduled/',
         post.status_scheduled,
         name='status_scheduled'),



    path('event/<int:event_id>/announcement/',
         post.event_announcement_create,
         name='event_announcement_create'),

    path('rsvp/convert/<int:rsvp_id>',
         post.rsvp_convert,
         name='rsvp_convert'),

        ]

from django.urls import path
from share import views


app_name = 'share'

urlpatterns = [
        path('embedded/<int:event_id>/', views.embedded, name='embedded'),

        path('event/<int:event_id>/rsvp/',
             views.event_rsvp,
             name='event_rsvp'),

        path('event/<int:event_id>/a/rsvp/',
             views.authenticated_rsvp,
             name='auth_rsvp'),

        path('event/<int:event_id>/b/rsvp/',
             views.anonymous_rsvp,
             name='no_auth_rsvp'),
]



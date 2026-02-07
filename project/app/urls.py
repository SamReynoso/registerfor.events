from django.urls import path
from app import user_views
from app import host_views
from app import participant_views


app_name = 'app'

urlpatterns = [
    path('profile/update-picture',
         user_views.profile_picture_update,
         name='profile_picture_update'),
    path('profile/update', user_views.profile_update, name='profile_update'),


    path('event/create', host_views.event_create, name='event_create'),
    path('event-divisions/<int:event_id>',
         host_views.event_divisions,
         name='event_divisions'),
    path('event/participant/<int:registration_id>',
         host_views.participant_edit,
         name='participant_edit'),


    path('team/create', participant_views.team_create, name='team_create'),
    path('register-for-event/<int:event_id>',
         participant_views.register_for_event,
         name='register_for_event'),
    path('registration/withdraw/<int:registration_id>',
         participant_views.registration_withdraw,
         name='registration_withdraw')
]

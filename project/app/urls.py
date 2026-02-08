from django.urls import path
from app import user_views
from app import host_views
from app import participant_views


app_name = 'app'

urlpatterns = [
    path('profile/update',
         user_views.profile_update,
         name='profile_update'),
    path('profile/delete',
         user_views.profile_delete,
         name='profile_delete'),

    path('profile/avatar/update',
         user_views.profile_avatar_update,
         name='profile_avatar_update'),
    path('profile/avatar/delete',
         user_views.profile_avatar_delete,
         name='profile_avatar_delete'),


    path('event/create',
         host_views.event_create,
         name='event_create'),
    path('event/<int:event_id>/update',
         host_views.event_update,
         name='event_update'),
    path('event/<int:event_id>/delete',
         host_views.event_delete,
         name='event_delete'),

    path('event/<int:event_id>/poster/update',
         host_views.event_poster_update,
         name='event_poster_update'),
    path('event/<int:event_id>/poster/delete',
         host_views.event_poster_delete,
         name='event_poster_delete'),

    path('event-divisions/<int:event_id>',
         host_views.event_divisions,
         name='event_divisions'),
    path('event/participant/<int:registration_id>',
         host_views.participant_edit,
         name='participant_edit'),
    path('event/<int:event_id>/status/',
         host_views.event_status,
         name='event_status'),
    path('event/<int:event_id>/announcement/',
         host_views.event_announcement,
         name='event_announcement'),

    path('team/create',
         participant_views.team_create,
         name='team_create'),
    path('team/<int:team_id>/update',
         participant_views.team_update,
         name='team_update'),
    path('team/<int:team_id>/delete',
         participant_views.team_delete,
         name='team_delete'),

    path('team/<int:team_id>/photo/update',
         participant_views.team_photo_update,
         name='team_photo_update'),
    path('team/<int:team_id>/photo/delete',
         participant_views.team_photo_delete,
         name='team_photo_delete'),

    path('register-for-event/<int:event_id>',
         participant_views.register_for_event,
         name='register_for_event'),
    path('registration/withdraw/<int:registration_id>',
         participant_views.registration_withdraw,
         name='registration_withdraw'),
    path('/announcement/<int:announcement_id>/delete/',
         participant_views.announcement_delete,
         name='announcement_delete'),



]

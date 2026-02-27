from django.urls import path
from play import views
from play import post


app_name = 'play'

urlpatterns = [
    path('',
         views.events,
         name='events'),

    path('teams/<int:team_id>/',
         views.team,
         name='team'),

    path('teams/',
         views.teams,
         name='teams'),

    path('registration/<int:registration_id>/',
         views.registration,
         name='registration'),

    path('registration/item/<int:registration_item_id>/',
         views.registration_item,
         name='registration_item'),

] + [
    path('team/create/',
         post.team_create,
         name='team_create'),
    path('team/<int:team_id>/update/',
         post.team_update,
         name='team_update'),
    path('team/<int:team_id>/delete/',
         post.team_delete,
         name='team_delete'),

    path('team/<int:team_id>/photo/update/',
         post.team_photo_update,
         name='team_photo_update'),
    path('team/<int:team_id>/photo/delete/',
         post.team_photo_delete,
         name='team_photo_delete'),

    path('register-for-event/<int:event_id>/',
         post.register_for_event,
         name='register_for_event'),
    path('registration/withdraw/<int:registration_id>/',
         post.withdraw,
         name='withdraw'),
    ]

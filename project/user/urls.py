from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('', views.account, name='account'),
    path('events/', views.events, name='events'),
    path('teams/', views.teams, name='teams'),
    path('hosting/', views.hosting, name='hosting'),
    path('participants/', views.participants, name='participants'),
    path('profile/', views.profile, name='profile'),

    path('event-details/<int:event_id>',
         views.event_details,
         name='event_details'),

    path('team-details/<int:team_id>',
         views.team_details,
         name='team_details'),

    path('registration_details/<int:registration_id>',
         views.registration_details,
         name='registration_details'),
]

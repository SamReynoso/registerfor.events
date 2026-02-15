from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('', views.account, name='account'),
    path('profile/', views.profile, name='profile'),

    path('events/', views.events, name='events'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>',
         views.team_details,
         name='team_details'),
    path('registration/<int:registration_id>',
         views.registration_details,
         name='registration_details'),

    path('hosting/', views.hosting, name='hosting'),
    path('hosting/event/<int:event_id>',
         views.hosting_event,
         name='hosting_event'),
    path('hosting/event/division/<int:division_id>/',
         views.hosting_division,
         name='hosting_division'),
    path('hosting/event/invitations/<int:event_id>',
         views.hosting_invitations,
         name='hosting_invitations'),
]

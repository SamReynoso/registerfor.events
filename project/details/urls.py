from django.urls import path
from details import views


app_name = 'details'

urlpatterns = [
        path('event/<int:event_id>', views.event, name='event'),
        path('team/<int:team_id>', views.team, name='team'),
        # path('host', views.host, name='host'),
        # path('teams', views.teams, name='teams'),
]

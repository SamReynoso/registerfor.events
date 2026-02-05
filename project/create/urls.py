from django.urls import path
from create import views


app_name = 'create'

urlpatterns = [
    path('', views.create, name='create'),
    path('events', views.events, name='events'),
    path('teams', views.teams, name='teams'),
    path('register/<int:event_id>',
         views.register_for_event,
         name='register_for_event'),
    # path('host', views.host, name='host'),
    # path('teams', views.teams, name='teams'),
]

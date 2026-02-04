from django.urls import path
from create import views


app_name = 'create'

urlpatterns = [
    path('', views.create, name='create'),
    path('events', views.events, name='events'),
    path('teams', views.teams, name='teams'),
    # path('host', views.host, name='host'),
    # path('teams', views.teams, name='teams'),
]

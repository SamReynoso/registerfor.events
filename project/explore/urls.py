from django.urls import path
from explore import views


app_name = 'explore'

urlpatterns = [
        path('event/<int:event_id>/', views.event, name='event'),
        path('team/<int:team_id>/', views.team, name='team'),
        path('division/<int:division_id>/', views.division, name='division'),
        path('profile/<int:profile_id>/', views.profile, name='profile'),
        path('search/', views.search_results, name='search_results'),
]

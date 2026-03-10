from django.urls import path
from pricing import views

app_name = 'pricing'

urlpatterns = [
        path('<int:event_id>/', views.pricing, name='pricing'),
        path('<int:event_id>/default', views.default, name='default'),
        path('<int:event_id>/divisions', views.divisions, name='divisions'),
        ]

from django.urls import path
from pricing import views

app_name = 'pricing'

urlpatterns = [
        path('<int:event_id>/', views.pricing, name='pricing'),
        path('<int:event_id>/default/', views.default, name='default'),
        path('<int:event_id>/divisions/', views.divisions, name='divisions'),
        path('divisions/<int:division_id>/', views.division, name='division'),
        path('registration/<int:registration_id>/', views.registration, name='registration'),
        path('item/<int:registration_item_id>/', views.registration_item, name='item'),
        ]

from django.urls import path
from share import views


app_name = 'share'

urlpatterns = [
        path('embedded/<int:event_id>/', views.embedded, name='embedded'),

        path('event/<int:event_id>/invite/',
             views.event_invite,
             name='event_invite'),
]



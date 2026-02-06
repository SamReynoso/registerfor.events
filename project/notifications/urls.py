from django.urls import path
from notifications import views


app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('convo/<int:profile_id>',
         views.conversation_view,
         name='conversation'),
    path('dm/', views.direct_messages_view, name='direct_messages'),
]

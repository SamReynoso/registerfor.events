from django.urls import path
from notifications import views


app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('dm/', views.direct_messages, name='direct_messages'),
    path('announcements/', views.announcements, name='announcements'),
    path('convo/<int:profile_id>', views.conversation_view, name='conversation'),
]

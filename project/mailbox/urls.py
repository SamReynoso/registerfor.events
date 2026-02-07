from django.urls import path
from mailbox import views


app_name = 'mailbox'

urlpatterns = [
    path('', views.mailbox, name='mailbox'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('convo/<int:profile_id>',
         views.conversation_view,
         name='conversation'),
    path('dm/', views.direct_messages_view, name='direct_messages'),
]

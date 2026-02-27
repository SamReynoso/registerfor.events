from django.urls import path


app_name = 'invite'

urlpatterns = [
    path('event/<int:event_id>/invite/',
         invite.event_invite,
         name='event_invite'),


]

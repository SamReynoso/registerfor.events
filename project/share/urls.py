from django.urls import path
from share import views


app_name = 'share'

urlpatterns = [

    path('rsvp/convert/<int:rsvp_id>',
         views.rsvp_convert,
         name='rsvp_convert'),

]

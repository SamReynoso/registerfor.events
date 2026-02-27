from django.urls import path
from user import views
from user import post


app_name = 'user'

urlpatterns = [
    path('',
         views.account,
         name='account'),

    path('profile/',
         views.profile,
         name='profile'),

] + [

    path('profile/update/',
         post.profile_update,
         name='profile_update'),
    path('profile/delete',
         post.profile_delete,
         name='profile_delete'),

    path('profile/avatar/update/',
         post.profile_avatar_update,
         name='profile_avatar_update'),
    path('profile/avatar/delete/',
         post.profile_avatar_delete,
         name='profile_avatar_delete'),
    ]

from django.urls import path
from base import views


app_name = 'base'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('verify/<str:uidb64>/<str:token>/',
         views.verify_email,
         name="verify_email"),
]

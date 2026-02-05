from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('account/', include('user.urls')),
    path('create/', include('create.urls')),
    path('details/', include('details.urls')),
    path('notifications/', include('notifications.urls')),
]

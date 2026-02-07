from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('account/', include('user.urls')),
    path('app/', include('app.urls')),
    path('details/', include('details.urls')),
    path('mailbox/', include('mailbox.urls')),
]

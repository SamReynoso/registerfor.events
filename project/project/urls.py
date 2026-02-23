from django.contrib import admin
from django.urls import path, include

from project import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('base.urls')),
    path('account/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('details/', include('details.urls')),
    path('mailbox/', include('mailbox.urls')),
    path('records/', include('records.urls')),

    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             email_template_name="registration/password_reset_email.txt",
             html_email_template_name="registration/password_reset_email.html",
             ),
         name="password_reset"),

    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.ASSET_URL,
                          document_root=settings.ASSET_ROOT)

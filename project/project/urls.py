from django.contrib import admin
from django.urls import path, include

from project import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('base.urls')),
    path('explore/', include('explore.urls')),

    path('account/', include('user.urls')),
    path('play/', include('play.urls')),
    path('host/', include('host.urls')),

    path('mailbox/', include('mailbox.urls')),
    path('pricing/', include('pricing.urls')),
    path('invoice/', include('invoice.urls')),
    path('share/', include('share.urls')),
    path('app/', include('app.urls')),

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

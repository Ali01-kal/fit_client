from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.views import RateLimitedLoginView
from core import views as core_views

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("core.urls", "core"), namespace="core")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("clients/", include(("clients.urls", "clients"), namespace="clients")),
    path("programs/", include(("programs.urls", "programs"), namespace="programs")),
    path(
        "memberships/",
        include(("memberships.urls", "memberships"), namespace="memberships"),
    ),
    path(
        "appointments/",
        include(("appointments.urls", "appointments"), namespace="appointments"),
    ),
    path("reviews/", include(("reviews.urls", "reviews"), namespace="reviews")),
    path("reports/", include(("reports.urls", "reports"), namespace="reports")),
    path("api/", include(("api.urls", "api"), namespace="api")),
    path(
        "login/",
        RateLimitedLoginView.as_view(),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("health/", core_views.healthcheck, name="healthcheck"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

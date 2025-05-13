from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("singup/", views.user_singup, name="singup"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
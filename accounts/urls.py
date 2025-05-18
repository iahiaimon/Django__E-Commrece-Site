from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("singup/", views.user_singup, name="singup"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/" , views.user_profile , name = "user_profile"),
]
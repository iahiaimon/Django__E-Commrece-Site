from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("singup/", views.user_singup, name="singup"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]

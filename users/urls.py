from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    RegisterView,
    ProfileView,
    email_verification,
    PasswordResetView,
    UserListView,
    UserUpdateView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("email-confirm/<str:token>/", email_verification, name="email_verification"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("user/edit/<int:pk>", UserUpdateView.as_view(), name="user_update"),
]

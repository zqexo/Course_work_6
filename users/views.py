import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm, UserForm
from users.models import User

from mailing.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        user.token = token
        user.save()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Добро пожаловать на сайт! Для подтверждения регистрации перейди по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetView(View):
    form_class = PasswordResetForm
    template_name = "users/password_reset.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                new_password = User.objects.make_random_password()
                user.password = make_password(new_password)
                user.save()

                send_mail(
                    subject="Восстановление пароля",
                    message=f"Ваш новый пароль: {new_password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[email],
                )
                return redirect(reverse("users:login"))
            except User.DoesNotExist:
                form.add_error("email", "Пользователь с таким email не найден")
        return render(request, self.template_name, {"form": form})


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.can_view_users_list"


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    permission_required = "users.can_block_user"
    success_url = reverse_lazy("users:user_list")

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.cache import cache

from blog.models import Blog
from blog.services import get_blogs_from_cache
from main.forms import ClientForm, MessageForm, MailingForm, ManagerMailingForm
from main.models import Client, Message, Mailing

from random import sample


@login_required
def homepage(request):
    # Получение данных из кэша или базы данных
    total_mailings = cache.get("total_mailings")
    if total_mailings is None:
        total_mailings = Mailing.objects.count()
        cache.set("total_mailings", total_mailings)

    active_mailings = cache.get("is_active_mailings")
    if active_mailings is None:
        active_mailings = Mailing.objects.filter(is_active=True).count()
        cache.set("active_mailings", active_mailings)

    unique_clients = cache.get("unique_clients")
    if unique_clients is None:
        unique_clients = Client.objects.count()
        cache.set("unique_clients", unique_clients)

    random_blogs = cache.get("random_blogs")
    if random_blogs is None:
        blogs = list(get_blogs_from_cache())  # Преобразуем QuerySet в список
        if len(blogs) > 3:
            random_blogs = sample(blogs, 3)  # Выбираем 3 случайных блога
        else:
            random_blogs = blogs  # Если меньше 3 блогов, выбираем все
        cache.set("random_blogs", random_blogs)

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
        "random_blogs": random_blogs,
    }

    return render(request, "main/homepage.html", context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {"title": "Клиенты"}

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("main.can_view_clients"):
            return Client.objects.all()
        else:
            return Client.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_view_clients"] = self.request.user.has_perm("main.can_view_client")
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:client_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        cache.clear()
        response = super().form_valid(form)
        form.instance.user = self.request.user
        return response


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:client_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()

        if (
            client.user == request.user
            or request.user.has_perm("main.can_change_clients")
            or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this client.")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("main:client_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if (
            client.user == request.user
            or request.user.has_perm("main.can_delete_clients")
            or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to delete this client.")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {"title": "Сообщения"}


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = "main.can_delete_message"
    success_url = reverse_lazy("main:message_list")

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to delete this message.")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this message.")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")

    def form_valid(self, form):
        cache.clear()
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("main.can_view_mailing"):
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_view_mailing"] = self.request.user.has_perm(
            "main.can_view_mailing"
        )
        context["can_change_mailing"] = self.request.user.has_perm(
            "main.can_change_mailing"
        )
        context["can_delete_mailing"] = self.request.user.has_perm(
            "main.can_delete_mailing"
        )
        context["can_switch_mailing"] = self.request.user.has_perm(
            "main.can_switch_mailing"
        )
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("main:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.has_perm("main.can_switch_mailing")
            and not request.user.is_superuser
        ):
            raise PermissionDenied("You do not have permission to add a new mailing.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["initial_send_date"] = now()
        kwargs["initial_end_date"] = now()
        return kwargs

    def form_valid(self, form):
        cache.clear()

        # Установите пользователя для формы перед сохранением
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Убедитесь, что форма уже сохранена и можно привязать клиентов
        clients_ids = self.request.POST.getlist("clients")
        form.instance.clients.set(clients_ids)

        return response


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy("main:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if (
            mailing.user == request.user
            or request.user.has_perm("main.can_change_mailing")
            or request.user.has_perm("main.can_switch_mailing")
            or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this mailing.")

    def get_form_class(self):
        if (
            self.request.user.has_perm("main.can_switch_mailing")
            and not self.request.user.is_superuser
        ):
            return ManagerMailingForm
        return MailingForm

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("main:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if (
            mailing.user == request.user
            or request.user.has_perm("main.can_delete_mailing")
            or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to delete this mailing.")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from main.forms import ClientForm, MessageForm, MailingForm
from main.models import Client, Message, Mailing


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
        context["can_view_clients"] = self.request.user.has_perm(
            "main.can_view_client"
        )
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
        response = super().form_valid(form)
        form.instance.user = self.request.user
        return response


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:client_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if client.user == request.user or \
                request.user.has_perm("main.can_change_clients") or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this client.")


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("main:client_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if client.user == request.user or \
                request.user.has_perm("main.can_delete_clients") or \
                request.user.is_superuser:
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


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this message.")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")

    def form_valid(self, form):
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
        context["can_view_mailing"] = self.request.user.has_perm("main.can_view_mailing")
        context["can_change_mailing"] = self.request.user.has_perm("main.can_change_mailing")
        context["can_delete_mailing"] = self.request.user.has_perm("main.can_delete_mailing")
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy("main:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["initial_send_date"] = now()
        kwargs["initial_end_date"] = now()
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.user = self.request.user
        form.instance.clients.set(self.request.POST.getlist("email"))
        return response


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy("main:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.user == request.user or \
                request.user.has_perm("main.can_change_mailing") or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to edit this mailing.")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("main:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.user == request.user or \
                request.user.has_perm("main.can_delete_mailing") or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to delete this mailing.")

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from main.forms import ClientForm, MessageForm, MailingForm
from main.models import Client, Message, Mailing


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {"title": "Клиенты"}


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:client_list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("main:client_list")


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("main:client_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {"title": "Сообщения"}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("main:message_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("main:message_list")


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {"title": "Рассылки"}


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("main:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial_send_date'] = now()
        kwargs['initial_end_date'] = now()
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.email.set(self.request.POST.getlist('email'))
        return response


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("main:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("main:mailing_list")

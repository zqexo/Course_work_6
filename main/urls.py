from main.apps import MainConfig
from django.urls import path

from main.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingListView,
    MailingUpdateView,
    MailingCreateView,
    MailingDeleteView,
    homepage,
)

app_name = MainConfig.name

urlpatterns = [
    path("", homepage, name="homepage"),
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/new", ClientCreateView.as_view(), name="client_create"),
    path("client/edit/<int:pk>", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>", ClientDeleteView.as_view(), name="client_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/new", MessageCreateView.as_view(), name="message_create"),
    path("message/edit/<int:pk>", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/new", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/edit/<int:pk>", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>", MailingDeleteView.as_view(), name="mailing_delete"),
]

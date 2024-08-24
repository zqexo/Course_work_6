from main.apps import MainConfig
from django.urls import path

from main.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = MainConfig.name

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("client/new", ClientCreateView.as_view(), name="client_create"),
    path("client/edit/<int:pk>", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>", ClientDeleteView.as_view(), name="client_delete"),
]

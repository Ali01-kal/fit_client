from django.urls import path

from .views import (
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientUpdateView,
    client_list,
    toggle_client_favorite,
)

urlpatterns = [
    path("", client_list, name="list"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("<slug:slug>/", ClientDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", ClientUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", ClientDeleteView.as_view(), name="delete"),
    path("<slug:slug>/favorite/", toggle_client_favorite, name="favorite"),
]

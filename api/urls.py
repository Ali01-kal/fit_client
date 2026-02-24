from django.urls import path

from .views import (
    api_client_detail,
    api_clients,
    api_program_detail,
    api_programs,
    api_reviews,
    api_stats,
    api_subscriptions,
)

urlpatterns = [
    path("clients/", api_clients, name="clients"),
    path("clients/<slug:slug>/", api_client_detail, name="client_detail"),
    path("programs/", api_programs, name="programs"),
    path("programs/<slug:slug>/", api_program_detail, name="program_detail"),
    path("subscriptions/", api_subscriptions, name="subscriptions"),
    path("reviews/", api_reviews, name="reviews"),
    path("stats/", api_stats, name="stats"),
]

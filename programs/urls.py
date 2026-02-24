from django.urls import path

from .views import ProgramCreateView, ProgramDetailView, ProgramUpdateView, program_list

urlpatterns = [
    path("", program_list, name="list"),
    path("create/", ProgramCreateView.as_view(), name="create"),
    path("<slug:slug>/", ProgramDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", ProgramUpdateView.as_view(), name="edit"),
]

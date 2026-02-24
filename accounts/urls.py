from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView, RegisterView, profile_redirect

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", profile_redirect, name="me"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]

from django.urls import path

from .views import ReviewCreateView, review_list

urlpatterns = [
    path("", review_list, name="list"),
    path("create/", ReviewCreateView.as_view(), name="create"),
]

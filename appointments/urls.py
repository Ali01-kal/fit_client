from django.urls import path

from .views import AppointmentCalendarView

urlpatterns = [
    path("", AppointmentCalendarView.as_view(), name="calendar"),
]

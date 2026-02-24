from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import Appointment


class AppointmentCalendarView(LoginRequiredMixin, View):
    template_name = "appointments/calendar.html"

    def get(self, request):
        appointments = Appointment.objects.select_related("client", "trainer").order_by("starts_at")[:30]
        return render(request, self.template_name, {"appointments": appointments})

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("client", "trainer", "starts_at", "status")
    list_filter = ("status", "trainer")
    search_fields = ("client__name", "trainer__name", "purpose")

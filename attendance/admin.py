from django.contrib import admin

from .models import CheckIn, SessionAttendance


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ("client", "checked_in_at", "source")
    list_filter = ("source",)
    search_fields = ("client__name",)


@admin.register(SessionAttendance)
class SessionAttendanceAdmin(admin.ModelAdmin):
    list_display = ("client", "session", "status")
    list_filter = ("status", "session__program")

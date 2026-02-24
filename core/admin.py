from django.contrib import admin

from .models import SiteContent


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("title", "maintenance_mode", "updated_at")
    list_filter = ("maintenance_mode",)
    readonly_fields = ("created_at", "updated_at")

from django.contrib import admin

from .models import ExportJob


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ("export_type", "status", "requested_by", "created_at")
    list_filter = ("status", "export_type")
    search_fields = ("requested_by", "export_type")

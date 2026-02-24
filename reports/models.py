from django.db import models

from core.models import TimeStampedModel


class ExportJob(TimeStampedModel):
    export_type = models.CharField(max_length=50)
    requested_by = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default="queued")
    file_path = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.export_type} ({self.status})"

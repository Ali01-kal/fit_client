from django.db import models

from clients.models import Client
from core.models import TimeStampedModel
from trainers.models import Trainer


class Appointment(TimeStampedModel):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="appointments"
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    purpose = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    class Meta:
        ordering = ("starts_at",)

    def __str__(self):
        return f"{self.client} / {self.trainer} @ {self.starts_at:%Y-%m-%d %H:%M}"

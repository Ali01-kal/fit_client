from django.db import models

from clients.models import Client
from core.models import TimeStampedModel
from programs.models import GroupSession


class CheckIn(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="checkins")
    checked_in_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=30, default="manual")

    class Meta:
        ordering = ("-checked_in_at",)

    def __str__(self):
        return f"{self.client.name} @ {self.checked_in_at:%Y-%m-%d %H:%M}"


class SessionAttendance(TimeStampedModel):
    STATUS_CHOICES = [
        ("booked", "Booked"),
        ("attended", "Attended"),
        ("missed", "Missed"),
        ("cancelled", "Cancelled"),
    ]
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="session_attendance"
    )
    session = models.ForeignKey(
        GroupSession, on_delete=models.CASCADE, related_name="attendances"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")

    class Meta:
        unique_together = ("client", "session")
        ordering = ("-session__starts_at",)

    def __str__(self):
        return f"{self.client} - {self.session} ({self.status})"

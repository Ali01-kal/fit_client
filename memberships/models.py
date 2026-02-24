from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import models

from clients.models import Client
from core.models import SluggedModel, TimeStampedModel


class MembershipPlan(SluggedModel, TimeStampedModel):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    visit_limit = models.PositiveIntegerField(default=12)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("price",)

    def __str__(self):
        return self.name


class Subscription(TimeStampedModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(
        MembershipPlan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    starts_on = models.DateField(default=date.today)
    ends_on = models.DateField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    visits_used = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-starts_on",)
        unique_together = ("client", "plan", "starts_on")

    def save(self, *args, **kwargs):
        if not self.ends_on:
            self.ends_on = self.starts_on + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def clean(self):
        if self.ends_on and self.ends_on <= self.starts_on:
            raise ValidationError({"ends_on": "Дата окончания должна быть позже начала."})

    def __str__(self):
        return f"{self.client.name} - {self.plan.name}"


class FreezeRequest(TimeStampedModel):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="freeze_requests"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ("-start_date",)

    def __str__(self):
        return f"Freeze {self.subscription} ({self.start_date})"

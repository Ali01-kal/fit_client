from django.db import models

from clients.models import Client
from core.models import TimeStampedModel
from memberships.models import Subscription


class Invoice(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-due_date",)

    def __str__(self):
        return f"Invoice #{self.pk} - {self.client.name}"


class Payment(TimeStampedModel):
    METHOD_CHOICES = [("cash", "Cash"), ("card", "Card"), ("transfer", "Transfer")]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.transaction_id} ({self.amount})"

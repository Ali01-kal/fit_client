from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import SluggedModel, TimeStampedModel, image_validators
from trainers.models import Trainer


class Client(SluggedModel, TimeStampedModel):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="client_record",
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    primary_trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, blank=True, null=True, related_name="clients"
    )
    avatar = models.ImageField(
        upload_to="clients/", blank=True, null=True, validators=image_validators()
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["name", "email"])]

    def __str__(self):
        return self.name

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def clean(self):
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError({"birth_date": "Дата рождения не может быть в будущем."})


class EmergencyContact(TimeStampedModel):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="emergency_contacts"
    )
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=60)

    class Meta:
        ordering = ("client", "full_name")

    def __str__(self):
        return f"{self.full_name} ({self.client.name})"


class HealthMetric(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="metrics")
    measured_at = models.DateField(default=date.today)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    body_fat_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    bmi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ("-measured_at",)

    def __str__(self):
        return f"{self.client.name} {self.measured_at}"


class ClientFavorite(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_clients"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("user", "client")

    def __str__(self):
        return f"{self.user} -> {self.client}"

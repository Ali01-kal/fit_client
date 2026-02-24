from django.core.exceptions import ValidationError
from django.db import models

from clients.models import Client
from core.models import TimeStampedModel
from programs.models import Program
from trainers.models import Trainer


class Review(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reviews")
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews"
    )
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.client} {self.rating}/5"

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError({"rating": "Рейтинг должен быть от 1 до 5."})

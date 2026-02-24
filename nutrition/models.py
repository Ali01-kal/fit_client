from django.core.exceptions import ValidationError
from django.db import models

from clients.models import Client
from core.models import TimeStampedModel
from trainers.models import Trainer


class MealPlan(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="meal_plans")
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, null=True, related_name="meal_plans"
    )
    title = models.CharField(max_length=120)
    calories_target = models.PositiveIntegerField()
    protein_grams = models.PositiveIntegerField(default=0)
    carbs_grams = models.PositiveIntegerField(default=0)
    fats_grams = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.client} - {self.title}"

    def clean(self):
        if self.calories_target < 800:
            raise ValidationError({"calories_target": "Слишком низкий калораж."})


class NutritionLog(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="nutrition_logs")
    logged_on = models.DateField()
    calories = models.PositiveIntegerField()
    water_ml = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-logged_on",)
        unique_together = ("client", "logged_on")

    def __str__(self):
        return f"{self.client} {self.logged_on}"

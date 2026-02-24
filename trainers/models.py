from django.db import models

from core.models import SluggedModel, TimeStampedModel, image_validators


class Trainer(SluggedModel, TimeStampedModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=120)
    experience_years = models.PositiveIntegerField(default=1)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    photo = models.ImageField(
        upload_to="trainers/", blank=True, null=True, validators=image_validators()
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class TrainerAvailability(TimeStampedModel):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="slots")
    weekday = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ("trainer", "weekday", "start_time")
        unique_together = ("trainer", "weekday", "start_time", "end_time")

    def __str__(self):
        return f"{self.trainer} {self.weekday} {self.start_time}-{self.end_time}"

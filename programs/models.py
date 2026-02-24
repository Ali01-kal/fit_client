from django.core.exceptions import ValidationError
from django.db import models

from core.models import SluggedModel, TimeStampedModel
from trainers.models import Trainer


class ProgramCategory(SluggedModel, TimeStampedModel):
    color = models.CharField(max_length=20, default="#1f8efa")

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Program categories"

    def __str__(self):
        return self.name


class Equipment(SluggedModel, TimeStampedModel):
    quantity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Program(SluggedModel, TimeStampedModel):
    DIFFICULTY_CHOICES = [("beginner", "Beginner"), ("mid", "Intermediate"), ("pro", "Pro")]
    description = models.TextField()
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, null=True, related_name="programs"
    )
    category = models.ForeignKey(
        ProgramCategory, on_delete=models.SET_NULL, null=True, related_name="programs"
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=60)
    max_clients = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    equipments = models.ManyToManyField(Equipment, blank=True, related_name="programs")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Exercise(TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=120)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=12)
    rest_seconds = models.PositiveIntegerField(default=60)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")
        unique_together = ("program", "name")

    def __str__(self):
        return f"{self.program.name}: {self.name}"


class GroupSession(TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="sessions")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    room = models.CharField(max_length=40, blank=True)
    capacity = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ("-starts_at",)

    def clean(self):
        if self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "Окончание должно быть позже начала."})

    def __str__(self):
        return f"{self.program.name} @ {self.starts_at:%Y-%m-%d %H:%M}"

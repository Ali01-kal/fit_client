from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel, image_validators


class UserProfile(TimeStampedModel):
    ROLE_CHOICES = [
        ("member", "Member"),
        ("trainer", "Trainer"),
        ("manager", "Manager"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, validators=image_validators()
    )
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ("user__username",)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def clean(self):
        if self.phone and not self.phone.replace("+", "").replace("-", "").isdigit():
            raise ValidationError({"phone": "Телефон должен содержать только цифры/+/ -"})

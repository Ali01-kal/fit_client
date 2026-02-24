from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=140, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base = slugify(self.name)[:120] or "item"
            slug = base
            i = 1
            Model = self.__class__
            while Model.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SiteContent(TimeStampedModel):
    title = models.CharField(max_length=120, default="fitClient")
    hero_text = models.TextField(default="Управление фитнес-клиентами и тренировками.")
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site content"
        verbose_name_plural = "Site content"

    def __str__(self):
        return self.title


def image_validators():
    return [FileExtensionValidator(["jpg", "jpeg", "png", "webp"])]

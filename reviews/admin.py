from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("client", "program", "trainer", "rating", "is_published")
    list_filter = ("rating", "is_published")
    search_fields = ("client__name", "comment", "program__name", "trainer__name")
    actions = ["publish_reviews", "unpublish_reviews"]

    @admin.action(description="Опубликовать")
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации")
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)

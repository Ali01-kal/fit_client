from django.contrib import admin

from .models import Trainer, TrainerAvailability


class TrainerAvailabilityInline(admin.TabularInline):
    model = TrainerAvailability
    extra = 1


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "experience_years", "is_active")
    list_filter = ("is_active", "specialization")
    search_fields = ("name", "email", "specialization")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TrainerAvailabilityInline]
    actions = ["mark_active", "mark_inactive"]

    @admin.action(description="Mark selected trainers active")
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected trainers inactive")
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(TrainerAvailability)
class TrainerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("trainer", "weekday", "start_time", "end_time")
    list_filter = ("weekday",)

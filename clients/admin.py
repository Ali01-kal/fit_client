from django.contrib import admin

from .models import Client, ClientFavorite, EmergencyContact, HealthMetric


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1


class HealthMetricInline(admin.TabularInline):
    model = HealthMetric
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "primary_trainer", "is_active")
    list_filter = ("is_active", "gender", "primary_trainer")
    search_fields = ("name", "email", "phone")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EmergencyContactInline, HealthMetricInline]
    fieldsets = (
        ("Основное", {"fields": ("name", "slug", "email", "phone", "gender", "birth_date")}),
        ("Тренировки", {"fields": ("primary_trainer", "is_active")}),
        ("Дополнительно", {"fields": ("avatar", "notes")}),
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("client", "full_name", "relation", "phone")
    search_fields = ("client__name", "full_name", "phone")


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ("client", "measured_at", "weight_kg", "body_fat_percent", "bmi")
    list_filter = ("measured_at",)


@admin.register(ClientFavorite)
class ClientFavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "created_at")
    search_fields = ("user__username", "client__name")
    list_filter = ("created_at",)

from django.contrib import admin

from .models import MealPlan, NutritionLog


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("client", "trainer", "title", "calories_target")
    search_fields = ("client__name", "title")


@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ("client", "logged_on", "calories", "water_ml")
    list_filter = ("logged_on",)

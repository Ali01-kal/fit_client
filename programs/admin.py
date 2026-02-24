from django.contrib import admin

from .models import Equipment, Exercise, GroupSession, Program, ProgramCategory


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "trainer", "category", "difficulty", "is_active")
    list_filter = ("difficulty", "is_active", "category")
    search_fields = ("name", "description", "trainer__name")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("equipments",)
    inlines = [ExerciseInline]
    actions = ["set_active", "set_inactive"]

    @admin.action(description="Сделать активными")
    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Сделать неактивными")
    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "is_available")
    list_filter = ("is_available",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("program", "name", "sets", "reps", "sort_order")
    list_filter = ("program",)
    search_fields = ("program__name", "name")


@admin.register(GroupSession)
class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ("program", "starts_at", "ends_at", "room", "capacity")
    list_filter = ("program", "starts_at")

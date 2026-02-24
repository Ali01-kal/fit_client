from django.contrib import admin

from .models import FreezeRequest, MembershipPlan, Subscription


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days", "visit_limit", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("client", "plan", "starts_on", "ends_on", "status", "visits_used")
    list_filter = ("status", "plan")
    search_fields = ("client__name", "client__email", "plan__name")


@admin.register(FreezeRequest)
class FreezeRequestAdmin(admin.ModelAdmin):
    list_display = ("subscription", "start_date", "end_date", "approved")
    list_filter = ("approved",)

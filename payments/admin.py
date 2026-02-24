from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "amount", "due_date", "is_paid")
    list_filter = ("is_paid", "due_date")
    search_fields = ("client__name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "invoice", "amount", "method", "created_at")
    list_filter = ("method",)
    search_fields = ("transaction_id", "invoice__client__name")

from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "category", "transaction_date", "created_at")
    list_filter = ("category", "transaction_date")
    search_fields = ("description", "user__username") 
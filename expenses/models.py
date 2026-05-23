from django.conf import settings
from django.db import models


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("travel", "Travel"),
        ("shopping", "Shopping"),
        ("education", "Education"),
        ("health", "Health"),
        ("bills", "Bills"),
        ("entertainment", "Entertainment"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"

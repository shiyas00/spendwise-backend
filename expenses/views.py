from django.db.models import Sum, Count, Max
from django.utils import timezone
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Expense
from .serializers import ExpenseSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "transaction_date"]
    search_fields = ["description", "category"]
    ordering_fields = ["amount", "transaction_date", "created_at"]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseSummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
        total_transactions = expenses.aggregate(count=Count("id"))["count"] or 0
        highest_expense = expenses.aggregate(max_amount=Max("amount"))["max_amount"] or 0

        today = timezone.now().date()
        monthly_expenses = expenses.filter(
            transaction_date__year=today.year,
            transaction_date__month=today.month
        )
        monthly_total = monthly_expenses.aggregate(total=Sum("amount"))["total"] or 0

        category_summary = (
            expenses
            .values("category")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )

        recent_expenses = ExpenseSerializer(expenses[:5], many=True).data

        return Response({
            "total_expense": total_expense,
            "monthly_total": monthly_total,
            "total_transactions": total_transactions,
            "highest_expense": highest_expense,
            "category_summary": category_summary,
            "recent_expenses": recent_expenses,
        })
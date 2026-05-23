from django.urls import path
from .views import RegisterView, ExpenseListCreateView, ExpenseDetailView, ExpenseSummaryView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("summary/", ExpenseSummaryView.as_view(), name="expense-summary"),
]
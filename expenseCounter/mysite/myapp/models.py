from django.db import models
from django.contrib.auth.models import User
import django_filters


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(default="No description")
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username if self.user else 'No User'} - {self.amount}"


class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    users = models.ManyToManyField(User)
    def split_expense(self):
        return self.amount / self.users.count()


class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Expense
        fields = ['date', 'category']

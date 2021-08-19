from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=100)
    currency = models.CharField(max_length=50)
    symbol = models.CharField(max_length=11, null=True)
    initial_balance = models.IntegerField()
    adjust_balance = models.IntegerField(null=True)
    freeze = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wallet_name

class Budget(models.Model):

    MONTH_YEAR = str(timezone.now().month) +'-'+ str(timezone.now().year)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    paycheck_income = models.IntegerField()
    extra_income = models.IntegerField(null=True)
    month = models.CharField(max_length=10, default=MONTH_YEAR, unique=True)
    
    def __str__(self):
        if self.extra_income:
            total = self.paycheck_income + self.extra_income
            return f'{total}'


class BillsPayments(models.Model):

    CATEGORY_CHOICES = (
        ('housing', 'Housing'),
        ('insurance', 'Insurance'),
        ('food', 'Food'),
        ('savings', 'Savings'),
        ('transportation', 'Transportation'),
        ('giving', 'Giving'),
        ('personal', 'Personal'),
        ('utilities', 'Utilities'),
        ('medical', 'Medical'),
        ('clothing', 'Clothing'),
        ('others', 'Others')
    )

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Choose a category')
    amount = models.IntegerField()
    expense_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description

class Transactions(models.Model):

    details = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(BillsPayments, null=True, on_delete=models.CASCADE)
    transaction_amount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.details

    

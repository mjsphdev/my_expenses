from django.db import models
from django.db.models.fields import DateField
from django.forms import ModelForm, DateInput
from .models import BillsPayments, Budget


class BillsPaymentsForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field is not 'expense_date':
                self.fields[field].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = BillsPayments
        fields = ['description', 'category', 'amount', 'expense_date']
        widgets = {
        'expense_date': DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


class BudgetForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Budget
        fields = ['paycheck_income', 'extra_income']

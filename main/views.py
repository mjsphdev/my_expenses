import json
from django.contrib.messages.api import info
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import BillsPaymentsForm, BudgetForm
from .models import BillsPayments, Transactions, Budget
from django.db.models import Sum

from django.contrib import messages
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

# Class Based Views
from django.views.generic import TemplateView, CreateView
from django.urls import reverse

class DashboardView(TemplateView):
    template_name = 'main/dashboard.html'
    
    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.request.user.id)
        wallet = user.budget_set.get(month='8-2021')

        now = timezone.now().strftime('%Y-%m-%d')
        month_year = timezone.now().strftime('%Y-%m')
        year = timezone.now().year

        transactions = user.billspayments_set.filter(expense_date=now)
        total_monthly_expense = user.billspayments_set.filter(expense_date__istartswith=month_year).aggregate(monthly_total=Sum('amount'))
        annual_expense = user.billspayments_set.filter(expense_date__istartswith=year).aggregate(annual_total=Sum('amount'))

        category = user.billspayments_set.values('category').filter(expense_date__istartswith=month_year).annotate(total=Sum('amount')).order_by('-total')
        data = json.dumps(list(category), cls=DjangoJSONEncoder)
    
        all_transactions = user.billspayments_set.filter(expense_date__lte=now)

        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'wallet': wallet,
            'transactions': transactions,
            'monthly': total_monthly_expense,
            'annual': annual_expense,
            'money_left': int(str(wallet)) - total_monthly_expense.get('monthly_total'),
            'category': data,
            'all_transactions': all_transactions
        })
        return context

class SetBudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.request.user.id)
        return super().form_valid(form)
    
    def get_success_url(self):
        http_referer = self.request.META.get('HTTP_REFERER').split('/')
        url = f'main:{http_referer[-2]}'
        return reverse(url)

class AddBillCreateView(CreateView):
    model = BillsPayments
    form_class = BillsPaymentsForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        http_referer = self.request.META.get('HTTP_REFERER').split('/')
        url = f'main:{http_referer[-2]}'
        return reverse(url)
         

@login_required(login_url='sign_in')
def update_bill(request, pk):
    bill = BillsPayments.objects.get(id=pk)
    form = BillsPaymentsForm(instance=bill)

    if request.method == 'POST':
        form = BillsPaymentsForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bills_payments')

    context = {'title': 'Update Bill', 'form': form}
    return render(request, 'main/add_bill.html', context)

@login_required(login_url='sign_in')
def delete_bill(request, pk):
    bill = BillsPayments.objects.get(id=pk)
    
    if request.method == 'POST':
        bill.delete()
        return redirect('bills_payments')
        
    context = {'title': 'Delete Bill', 'bill': bill}
    return render(request, 'main/delete_bill.html', context)

@login_required(login_url='sign_in')
def change_status(request, pk):
    bill = BillsPayments.objects.get(id=pk)

    if request.method == 'POST':
        BillsPayments.objects.filter(id=pk).update(status=1)
        bill = BillsPayments.objects.get(id=pk)
        Transactions.objects.create(details=bill.description, transaction_amount=bill.amount, transaction_status=1, bill_id=bill.id, user_id=request.user.id)
        return redirect('bills_payments')

    context = {'title': 'Change Status', 'bill': bill}
    return render(request, 'main/change_status.html', context)

@login_required(login_url='sign_in')
def budget(request):
    month_year = str(timezone.now().month) + ',' + str(timezone.now().year)

    money_expense = BillsPayments.objects.filter(month=month_year).aggregate(Sum('amount'))
    breakdowns = BillsPayments.objects.values('category').annotate(total_amount=Sum('amount')) \
                .annotate(percentage=(Sum('amount')/10000.00)*100).filter(month=month_year).order_by('-total_amount')

    try:
        Budget.objects.filter(month=month_year).update(total_expense=money_expense.get('amount__sum'))
        budget = Budget.objects.get(month=month_year)
        money_left = budget.budget - budget.total_expense
    except:
        budget = 0
        money_left = 0

    context = {'title': 'Budget', 'budget': budget, 'money_left': money_left, 'breakdowns': breakdowns}
    return render(request, 'main/budget.html', context)

@login_required(login_url='sign_in')
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = User.objects.get(pk=request.user.id)

            exist = Budget.objects.filter(month=budget.month)

            if exist:
                messages.warning(request, "You've already set a budget for this month.")
            else:
                budget.save()
                messages.success(request, 'Success!')
            return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='sign_in')
def profile(request):

    context = {'title': 'Profile'}
    return render(request, 'main/profile.html', context)


@login_required
def getdata(request):
    user = User.objects.get(pk=request.user.id)
    wallet = user.budget_set.get(month='8-2021')
    month_year = timezone.now().strftime('%Y-%m')
    
    category = user.billspayments_set.values('category').filter(expense_date__istartswith=month_year).annotate(total=Sum('amount')).order_by('-total')
    for c in category:
        print(c)

    command = request.POST['textResult']
    result = ''
    if 'budget report' in command:
        result = f"You have {wallet} for this month."
    elif 'give me' in command:
        result = "Here is the breakdown and percentage of your expenses for this month. "
        for c in category:
            result+= f"For the category of {c.get('category')}, you have a total of {c.get('total')} and this is {round((c.get('total')/int(str(wallet)))*100)}% of your budget. "
        result+="That's all master."

    else:
        result = 'Sorry, I did not get that'

    return HttpResponse(result)


from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(extra_context={'title': 'Dashboard'}), name='dashboard'),
    path('bills-payments/add-bills/', views.AddBillCreateView.as_view(), name='add_bill'),
    path('budget/set-budget/', views.SetBudgetCreateView.as_view(), name='set_budget'),
    path('profile/', views.profile, name='profile'),
    path('getdata/', views.getdata)
]
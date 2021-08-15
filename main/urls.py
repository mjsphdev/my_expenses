from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard/', views.dashboard, name='home'),
    path('bills-payments/', views.bills_payments, name='bills_payments'),
    path('bills-payments/add-bills/', views.add_bill, name='add_bill'),
    path('bills-payments/update-bill/<str:pk>/', views.update_bill, name='update_bill'),
    path('bills-payments/delete-bill/<str:pk>/', views.delete_bill, name='delete_bill'),
    path('bills-payments/change_status/<str:pk>/', views.change_status, name='change_status'),
    path('budget/', views.budget, name='budget'),
    path('budget/set_budget/', views.set_budget, name='set_budget'),
    path('profile/', views.profile, name='profile'),
    path('getdata/', views.getdata)
]
from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('redirect/', views.Redirect.as_view(), name='redirect'),
    path('dashboard/', views.DashboardView.as_view(extra_context={'title': 'Dashboard'}), name='dashboard'),
    path('my-wallet/', views.WalletView.as_view(extra_context={'title': 'Wallet'}), name='wallet'),
    path('create-wallet/', views.CreateWallet.as_view(), name='create_wallet'),
    path('get-wallet/', views.getwallet),
    path('my-wallet/get-wallet/detail/', views.getwalletdetail, name="wallet_detail"),
    path('my-wallet/freeze/', views.freeze_wallet, name='freeze_wallet'),
    path('my-wallet/delete/', views.delete_wallet, name='delete_wallet'),
    path('bills-payments/add-bills/', views.AddBillCreateView.as_view(), name='add_bill'),
    path('budget/set-budget/', views.SetBudgetCreateView.as_view(), name='set_budget'),
    path('profile/', views.profile, name='profile'),
    path('getdata/', views.getdata)
]
from django.urls import path
from . import views

urlpatterns = [
    path('v1/init', views.init_wallet, name='api-init'),
    path('v1/wallet', views.enable_wallet, name='api-wallet'),
    path('v1/wallet/deposits', views.deposit, name='api-deposit'),
    path('v1/wallet/withdrawals', views.withdraw, name='api-withdraw'),
    path('v1/wallet/transactions', views.api_transactions, name='api-list-transaction'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('v1/init', views.init_wallet),
    path('v1/wallet', views.enable_wallet),
]
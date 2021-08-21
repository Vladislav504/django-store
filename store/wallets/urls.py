from django.urls import path

from .views import WalletsRegisterView, WalletsLoginView, WalletsLogOutView, WalletsHomeView, WalletDetailView

urlpatterns = [
    path('me', WalletsHomeView.as_view(), name='home'),
    path('login', WalletsLoginView.as_view(), name='login'),
    path('logout', WalletsLogOutView.as_view(), name='logout'),
    path('register', WalletsRegisterView.as_view(), name='register'),
    path('<str:address>', WalletDetailView.as_view(), name='wallet_detail'),
]

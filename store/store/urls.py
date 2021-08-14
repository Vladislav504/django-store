from django.contrib import admin
from django.urls import path

from wallets.views import WalletsRegisterView, WalletsLoginView, WalletsLoggingOutView, WalletsHomeView
from goods.views import GoodsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GoodsView.as_view(), name='goods_list'),
    path('wallets', WalletsHomeView.as_view(), name='home'),
    path('wallets/register', WalletsRegisterView.as_view(), name='register'),
    path('wallets/login', WalletsLoginView.as_view(), name='login'),
    path('wallets/logout', WalletsLoggingOutView.as_view(), name='logout'),

]

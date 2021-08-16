from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse
from django.views.generic.base import RedirectView

from wallets.urls import urlpatterns as wallets_urls
from goods.urls import urlpatterns as goods_urls
from transactions.urls import urlpatterns as transactions_urls


def redirect2home(request):
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect2home),
    path('goods/', include(goods_urls)),
    path('wallets/', include(wallets_urls)),
    path('transactions/', include(transactions_urls)),
]

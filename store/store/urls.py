from django.contrib import admin
from django.urls import path, include

from wallets.urls import urls as wallets_urls
from goods.urls import urls as goods_urls
from transactions.urls import urls as transactions_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goods/', include(goods_urls)),
    path('wallets/', include(wallets_urls)),
    path('transactions/', include(transactions_urls)),
]

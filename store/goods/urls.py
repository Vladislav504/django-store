from django.urls import path

from .views import GoodsView, GoodView

urls = [
    path('', GoodsView.as_view(), name='goods_list'),
    path('<int:id>', GoodView.as_view(), name="goods_detail")
]
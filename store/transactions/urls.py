from django.urls import path

from .views import FundInView, BuyView, SellView

urls = [
    path('in', FundInView.as_view(), name='fundin'),
    path('<int:id>/buy', BuyView.as_view(), name='transaction_buy'),
    path('<int:id>/sell', SellView.as_view(), name='transaction_sell'),
]
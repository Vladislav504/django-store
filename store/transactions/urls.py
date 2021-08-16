from django.urls import path

from .views import ControlView, BuyView, SellView

urlpatterns = [
    path('in', ControlView.as_view(), name='control'),
    path('<int:id>/buy', BuyView.as_view(), name='transaction_buy'),
    path('<int:id>/sell', SellView.as_view(), name='transaction_sell'),
]
from django.urls import path

from .views import FundInView

urls = [
    path('in', FundInView.as_view(), name='fundin'),
]
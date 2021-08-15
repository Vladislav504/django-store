from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

from wallets.models import Wallet
from wallets.services import get_balance
from .models import Transaction

class FundInView(TemplateView):
    template_name = 'transactions/in.html'

    def get(self, request):
        wallet: Wallet = request.user
        balance = get_balance(wallet) if wallet.is_authenticated else 0
        return render(request, self.template_name, context={'balance': balance})
    
    def post(self, request):
        wallet = request.user
        try:
            price = float(request.POST['sum'])
        except ValueError:
            return HttpResponseBadRequest("Inappropriate value")
        if wallet.is_authenticated:
            Transaction(seller=wallet, price=price, completed=True).save()
        return HttpResponseRedirect(reverse('fundin'))

from django.core.checks.messages import Error
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from wallets.services import get_balance
from .models import Transaction
from store.utils import validate_price
from .services import validate_type, InvalidTypeOfTransaction, create_completed_transaction


class ControlView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/control.html'
    error = None

    def get(self, request):
        return render(request,
                      self.template_name,
                      context={'balance': get_balance(self.wallet)})

    def post(self, request):
        self.get_price()
        self.get_type()
        if self.error:
            return self.error
        create_completed_transaction(self.price, self.type_)
        return HttpResponseRedirect(reverse('control'))

    def get_price(self):
        try:
            self.price = validate_price(self.request.POST['price'])
        except ValueError:
            self.error = HttpResponseBadRequest("Inappropriate value")

    def get_type(self):
        try:
            self.type_ = self.request.POST['type']
            validate_type(self.type_)
        except InvalidTypeOfTransaction:
            self.error = HttpResponseBadRequest("Inappropriate type")


class BuyView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/buy.html'

    def get(self, request, id):
        trans = Transaction.objects.get(id=id)
        return render(request,
                      self.template_name,
                      context={'transaction': trans})

    def post(self, request, id):
        trans: Transaction = Transaction.objects.get(id=id)
        trans.buy_by(request.user)
        return HttpResponseRedirect(
            reverse('goods_detail', args=[trans.good.id]))


class SellView(TemplateView):
    template_name = 'transactions/sell.html'

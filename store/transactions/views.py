from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from wallets.services import get_balance
from .models import Transaction


class ControlView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/control.html'
    validator = float

    def dispatch(self, request, *args, **kwargs):
        self.wallet = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request,
                      self.template_name,
                      context={'balance': get_balance(self.wallet)})

    def post(self, request):
        price = self.validate_sum(request.POST['sum'])
        type_ = self.validate_type(request.POST['type'])
        self.create_transaction(price, type_)
        return HttpResponseRedirect(reverse('control'))

    def validate_sum(self, sum_: str):
        try:
            return self.validator(sum_)
        except ValueError:
            return self.validator(0)

    def validate_type(self, type_: str):
        if type_ not in ['in', 'out']:
            raise ValueError('Type is wrong.')
        return type_

    def create_transaction(self, price, type_):
        trans = Transaction(price=price, completed=True)
        trans = self.fill_or_withdraw(trans, type_)
        trans.save()

    def fill_or_withdraw(self, trans: Transaction, type_: str) -> Transaction:
        if type_ == 'in':
            trans.seller = self.wallet
        elif type_ == 'out':
            trans.buyer = self.wallet
        return trans


class BuyView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/buy.html'

    def get(self, request, id):
        trans = Transaction.objects.get(id=id)
        return render(request,
                      self.template_name,
                      context={'transaction': trans})

    def post(self, request, id):
        trans: Transaction = Transaction.objects.get(id=id)
        if not trans.completed:
            trans.buyer = request.user
            trans.completed = True
            trans.save()
        return HttpResponseRedirect(
            reverse('goods_detail', args=[trans.good.id]))


class SellView(TemplateView):
    template_name = 'transactions/sell.html'

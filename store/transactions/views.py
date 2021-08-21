from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .services import get_transaction
from .services import create_completed_transaction
from .services import validate_type, validate_price
from store.views import BaseView
from wallets.services import get_balance


class ControlView(LoginRequiredMixin, BaseView):
    template_name = 'transactions/control.html'
    error = None

    def get(self, request):
        return render(request,
                      self.template_name,
                      context={'balance': get_balance(request.user)})

    def post(self, request):
        price = validate_price(request.POST.get('price'))
        type_ = validate_type(request.POST.get('type'))
        create_completed_transaction(price, type_)
        return HttpResponseRedirect(reverse('control'))


class BuyView(LoginRequiredMixin, BaseView):
    template_name = 'transactions/buy.html'

    def get(self, request, id):
        trans = get_transaction(id)
        return render(request,
                      self.template_name,
                      context={'transaction': trans})

    def post(self, request, id):
        trans = get_transaction(id)
        trans.buy_by(request.user)
        return HttpResponseRedirect(
            reverse('goods_detail', args=[trans.good.id]))


class SellView(TemplateView):
    template_name = 'transactions/sell.html'

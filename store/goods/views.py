from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .models import Good
from .services import get_good
from transactions.services import validate_type, validate_price
from transactions.services import get_uncompleted_transactions
from transactions.services import create_uncompleted_transaction
from store.views import BaseView


class GoodsView(BaseView):
    template_name = 'goods/goods.html'

    def get(self, request):
        all_ = Good.objects.all()  # TODO: change to limit size
        return render(request, self.template_name, context={'goods': all_})


class GoodView(LoginRequiredMixin, BaseView):
    template_name = 'goods/good.html'

    def get(self, request, id):
        good = get_good(id)
        selling, buying = get_uncompleted_transactions()
        context = {'item': good, 'selling': selling, 'buying': buying}
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        good = get_good(id)
        price = validate_price(request.POST.get('price'))
        type_ = validate_type(request.POST.get('type'))
        create_uncompleted_transaction(request.user, type_, good, price)
        return HttpResponseRedirect(reverse('goods_detail', args=[id]))

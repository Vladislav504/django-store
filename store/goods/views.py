from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Good
from store.utils import validate_price
from transactions.services import InvalidTypeOfTransaction, validate_type
from transactions.services import get_uncompleted_transactions
from transactions.services import create_uncompleted_transaction


class GoodsView(TemplateView):
    template_name = 'goods/goods.html'

    def get(self, request):
        all_ = Good.objects.all()  # TODO: change to limit size
        return render(request, self.template_name, context={'goods': all_})


class GoodView(LoginRequiredMixin, TemplateView):
    template_name = 'goods/good.html'
    error = None

    def get(self, request, id):
        self.get_good(id)
        selling, buying = get_uncompleted_transactions()
        context = {'item': self.good, 'selling': selling, 'buying': buying}
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        self.get_good(id)
        self.get_price()
        self.get_type()
        if self.error:
            return self.error
        create_uncompleted_transaction(request.user, self.type_, self.good,
                                       self.price)
        return HttpResponseRedirect(reverse('goods_detail', args=[id]))

    def get_good(self, id):
        try:
            self.good = Good.objects.get(id=id)
        except Good.DoesNotExist:
            self.error = HttpResponseBadRequest('No such Good.')

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

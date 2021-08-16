from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .models import Good
from transactions.models import Transaction


class GoodsView(TemplateView):
    template_name = 'goods/goods.html'

    def get(self, request):
        all_ = Good.objects.all()  # TODO: change to limit size
        return render(request, self.template_name, context={'goods': all_})


class GoodView(LoginRequiredMixin, TemplateView):
    template_name = 'goods/good.html'

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            self.good = Good.objects.get(id=id)
        except Good.DoesNotExist:
            return HttpResponseBadRequest({})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        selling = Transaction.objects.filter(
            seller__isnull=False, completed=False,
            buyer__isnull=True).order_by('price')
        buying = Transaction.objects.filter(
            seller__isnull=True, completed=False,
            buyer__isnull=False).order_by('price')
        context = {'item': self.good, 'selling': selling, 'buying': buying}
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        try:
            price = float(request.POST['price'])
        except ValueError:
            return HttpResponseBadRequest("Inappropriate value")
        type_ = request.POST['type']
        trans = Transaction(good=self.good, completed=False, price=price)
        if type_ == 'sell':
            trans.seller = request.user
        elif type_ == 'buy':
            trans.buyer = request.user
        else:
            return HttpResponseBadRequest("Inappropriate type")
        trans.save()
        return HttpResponseRedirect(reverse('goods_detail', args=[id]))

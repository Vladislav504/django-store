from django.urls import reverse
from django.http.response import  HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Good
from transactions.models import Transaction

class GoodsView(TemplateView):
    template_name = 'goods/goods.html'

    def get(self, request):
        all_ = Good.objects.all()  # TODO: change to limit size
        return render(request, self.template_name, context={'goods': all_})


class GoodView(TemplateView):
    template_name = 'goods/good.html'

    def get(self, request, id):
        try:
            good = Good.objects.get(id=id)
        except Good.DoesNotExist:
            return HttpResponseBadRequest({})
        selling = Transaction.objects.filter(seller__isnull=False, completed=False, buyer__isnull=True)
        context = {'item': good, 'selling': selling}
        return render(request, self.template_name, context=context)
    

    def post(self, request, id):
        try:
            good = Good.objects.get(id=id)
        except Good.DoesNotExist:
            return HttpResponseBadRequest({})
        try:
            price = float(request.POST['price'])
        except ValueError:
            return HttpResponseBadRequest("Inappropriate value")
        Transaction(seller=request.user, good=good, completed=False, price=price).save()
        return HttpResponseRedirect(reverse('goods_detail', args=[id]))
        

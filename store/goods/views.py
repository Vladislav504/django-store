from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Good

class GoodsView(TemplateView):
    template_name = 'goods/goods.html'

    def get(self, request):
        all_ = Good.objects.all() # TODO: change to limit size
        
        return render(request, self.template_name, context={'goods': all_})
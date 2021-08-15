import json
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Wallet
from .services import get_balance


class WalletsHomeView(TemplateView):
    template_name = 'wallets/home.html'

    def get(self, request):
        balance = get_balance(
            request.user) if request.user.is_authenticated else 0.0

        return render(request,
                      self.template_name,
                      context={'balance': balance})


class WalletsRegisterView(TemplateView):
    template_name = 'wallets/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        password = request.POST['password']
        wallet = Wallet.create(password=password)
        login(request, wallet)
        return HttpResponseRedirect(reverse('home'))


class WalletsLoginView(TemplateView):
    template_name = 'wallets/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        address = request.POST['address']
        password = request.POST['password']
        wallet = authenticate(request=request,
                              address=address,
                              password=password)
        if wallet is None:
            return HttpResponseBadRequest(
                json.dumps({'message': "Bad auth data"}))
        login(request, wallet)
        return render(request, self.template_name)


class WalletsLoggingOutView(TemplateView):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

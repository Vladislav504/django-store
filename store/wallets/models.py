from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.apps import apps

from .managers import CustomUserManager


class Wallet(AbstractBaseUser):
    address = models.CharField(unique=True,
                               primary_key=True,
                               editable=False,
                               max_length=64,
                               null=False,
                               blank=False)

    USERNAME_FIELD = 'address'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @classmethod
    def create(cls, password):
        return cls.objects.create_wallet(password)

    @property
    def balance(self):
        Transaction = apps.get_model(app_label='transactions',
                                     model_name='Transaction')
        buyings = Transaction.objects.filter(buyer=self, completed=True)
        sells = Transaction.objects.filter(seller=self, completed=True)
        balance: int = 0
        for buy in buyings:
            balance -= buy.price
        for sell in sells:
            balance += sell.price
        return balance

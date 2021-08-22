from django.db import models

from wallets.models import Wallet
from goods.models import Good
from . import exceptions


class Transaction(models.Model):
    buyer = models.ForeignKey(Wallet,
                              on_delete=models.SET_NULL,
                              related_name='buyer',
                              null=True)
    seller = models.ForeignKey(Wallet,
                               on_delete=models.SET_NULL,
                               related_name='seller',
                               null=True)
    good = models.ForeignKey(Good,
                             on_delete=models.PROTECT,
                             null=True,
                             related_name='selling_goods')
    price = models.FloatField(null=False, default=0.0)

    completed = models.BooleanField(default=False)

    def complete(self):
        self.completed = True
        self.save(update_fields=['completed'])

    def buy_by(self, user):
        if not self.completed:
            if user.balance < self.price:
                raise exceptions.NotEnoughMoney(
                    'Not enough money on wallet to complete transaction.')
            self.buyer = user
            self.completed = True
            self.save(update_fields=['completed', 'buyer'])

    def save(self, *args, **kwargs):
        self.check_integrity()
        super().save(*args, **kwargs)

    def check_integrity(self):
        if self.seller is None and self.buyer is None:
            raise exceptions.SellerAndBuyerIsMissing(
                'No seller and buyer in transaction.')
        if self.seller == self.buyer:
            raise exceptions.SellerEqualBuyer("Seller cannot buy own goods.")

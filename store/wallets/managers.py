from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

import uuid


class CustomUserManager(BaseUserManager):
    def create_wallet(self, password, **extra_fields):
        address = uuid.uuid4().hex
        wallet = self.model(address=address, **extra_fields)
        wallet.set_password(password)
        wallet.save()
        return wallet
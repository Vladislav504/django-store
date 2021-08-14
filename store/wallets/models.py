
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager

class Wallet(AbstractBaseUser):
    address = models.CharField(unique=True, primary_key=True, editable=False, max_length=64, null=False, blank=False)

    USERNAME_FIELD = 'address'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @classmethod
    def create(cls, password):
        return cls.objects.create_wallet(password)

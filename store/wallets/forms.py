from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Wallet


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = Wallet


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Wallet
        fields = ('address',)
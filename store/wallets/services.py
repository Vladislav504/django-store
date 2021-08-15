
from transactions.models import Transaction
from .models import Wallet

def get_balance(wallet: Wallet) -> int:
    buyings = Transaction.objects.filter(buyer=wallet, completed=True)
    sells = Transaction.objects.filter(seller=wallet, completed=True)
    balance: int = 0
    for buy in buyings:
        balance -= buy.price
    for sell in sells:
        balance += sell.price
    return balance

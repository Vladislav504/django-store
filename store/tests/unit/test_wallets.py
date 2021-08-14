import pytest

from wallets.models import Wallet

pytestmark = pytest.mark.django_db

def test_wallet_creation():
    wallet: Wallet = Wallet.create('dunk_password')
    assert wallet.check_password('dunk_password')
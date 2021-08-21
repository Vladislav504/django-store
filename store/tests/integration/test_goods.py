import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from goods.models import Good
from transactions.models import Transaction

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_good():
    def good(**kwargs) -> Good:
        object = Good(**kwargs)
        object.save()
        return object

    return good


@pytest.fixture
def password():
    return 'password'


@pytest.fixture
def create_user(password):
    user_model = get_user_model()

    def user(**kwargs) -> user_model:
        user = user_model.objects.create_wallet(password=password, **kwargs)
        return user

    return user


@pytest.fixture
def good(create_good):
    return create_good(name='Test')


@pytest.fixture
def auto_login(client, create_user, password):
    def make_login(user=None):
        if user is None:
            user = create_user()
        client.login(address=user.address, password=password)
        return client, user

    return make_login


def test_unauthenticated_create_transaction_for_good(client, good):
    url = reverse('goods_detail', kwargs={'id': good.pk})
    payload = {'type_': 'sell', 'price': 1}
    response = client.post(url, data=payload)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_succsessfull_uncomplete_transaction_creation_for_good(
        auto_login, good):
    client, _ = auto_login()
    url = reverse('goods_detail', kwargs={'id': good.pk})
    payload = {'type': 'sell', 'price': 1}
    response = client.post(url, data=payload)
    assert response.status_code == 302
    assert response.url == url
    assert Transaction.objects.all().count() == 1

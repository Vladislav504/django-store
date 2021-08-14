import pytest

from goods.models import Good

pytestmark = pytest.mark.django_db

def test_good_creation():
    good = Good(name='Test')
    assert good.name == 'Test'
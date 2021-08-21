from store.exceptions import ResponseException
from .models import Transaction


class InvalidTypeOfTransaction(ResponseException):
    status = 400


class TransactionNotFound(ResponseException):
    status = 404


class InvalidTypeOfPrice(ResponseException):
    status = 400
    pass


def validate_price(price: str):
    try:
        return float(price)
    except Exception:
        raise InvalidTypeOfPrice('Invalid type of price!')


def validate_type(type_):
    if type_ not in ['sell', 'buy']:
        raise InvalidTypeOfTransaction('Invalid type of transaction type.')
    return type_


def create_uncompleted_transaction(user, type_, good, price):
    trans = Transaction(good=good, completed=False, price=price)
    validate_type(type_)
    if type_ == 'sell':
        trans.seller = user
    if type_ == 'buy':
        trans.buyer = user
    trans.save()
    return trans


def create_completed_transaction(user, type_, good, price):
    trans = create_uncompleted_transaction(user, type_, good, price)
    trans.complete()
    return trans


def get_uncompleted_transactions(good=None):
    selling = Transaction.objects.filter(seller__isnull=False,
                                         completed=False,
                                         buyer__isnull=True).order_by('price')
    buying = Transaction.objects.filter(seller__isnull=True,
                                        completed=False,
                                        buyer__isnull=False).order_by('price')
    if good is not None:
        selling = selling.filter(good=good)
        buying = buying.filter(good=good)
    return selling, buying


def get_transaction(id) -> Transaction:
    try:
        return Transaction.objects.get(id=id)
    except Transaction.DoesNotExist:
        raise TransactionNotFound('Transaction with such id does not found.')

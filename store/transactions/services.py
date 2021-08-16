from .models import Transaction


class InvalidTypeOfTransaction(Exception):
    pass


def validate_type(type_):
    if type_ not in ['sell', 'buy']:
        raise InvalidTypeOfTransaction()


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



def get_uncompleted_transactions():
    selling = Transaction.objects.filter(seller__isnull=False,
                                         completed=False,
                                         buyer__isnull=True).order_by('price')
    buying = Transaction.objects.filter(seller__isnull=True,
                                        completed=False,
                                        buyer__isnull=False).order_by('price')
    return selling, buying

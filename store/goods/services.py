from store.exceptions import ResponseException
from .models import Good


class GoodNotFound(ResponseException):
    status = 404
    pass


def get_good(id):
    try:
        return Good.objects.get(id=id)
    except Good.DoesNotExist:
        raise GoodNotFound('Good with such id not found')
from store.exceptions import ResponseException


class SellerEqualBuyer(ResponseException):
    status = 400


class SellerAndBuyerIsMissing(ResponseException):
    status = 400


class InvalidTypeOfTransaction(ResponseException):
    status = 400


class TransactionNotFound(ResponseException):
    status = 404


class InvalidTypeOfPrice(ResponseException):
    status = 400


class NotEnoughMoney(ResponseException):
    status = 400

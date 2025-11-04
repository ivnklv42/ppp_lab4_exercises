from enum import Enum
from money_functions import *


class Currency(Enum):
    Euro = 1
    USD = 2
    Ruble = 3

class Money:
    def __init__(self, currency: Currency, price):
        self.__currency = currency
        self.__price = price

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency: Currency):
        self.__currency = currency

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    def __add__(self, other):
        if not (isinstance(other, float) or isinstance(other, Money)):
            raise ArithmeticError("К объекту типа Money можно прибавить только число или объект типа Money")

        if isinstance(other, Money):
            check_currency(self, other)
            check_price(other.__price)
            self.__price += other.__price
        else:
            check_price(other)
            self.__price += other

        return self.__price

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, float) or isinstance(other, Money)):
            raise ArithmeticError("Из объекта типа Money можно отнять только число или объект типа Money")

        if isinstance(other, Money):
            check_currency(self, other)
            check_price(other.__price)
            self.__price -= other.__price
        else:
            check_price(other)
            self.__price -= other

        return self.__price

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if not isinstance(other, float):
            raise ArithmeticError("Объект типа Money можно умножить только на число")

        if other < 0 or other > 1_000_000:
            raise ValueError("Объект типа Money можно умножить на число, "
                             "которое больше или равно нулю и меньше миллиона")

        return self.__price * other

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        is_money(other)
        check_currency(self, other)
        return self.__price == other.__price

    def __lt__(self, other):
        is_money(other)
        check_currency(self, other)
        return self.__price < other.__price

    def __le__(self, other):
        is_money(other)
        check_currency(self, other)
        return self.__price <= other.__price

    def get_currency(self):
        match self.currency:
            case Currency.Euro:
                return "Euro"
            case Currency.USD:
                return "USD"
            case Currency.Ruble:
                return "Ruble"

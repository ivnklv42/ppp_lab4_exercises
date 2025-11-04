from entities import PricedEntity, DiscountableEntity
from money import Currency, Money
from enum import Enum


class Promotion(Enum):
    three_for_two = 1
    rubles_discount_10 = 2

class Product(DiscountableEntity, PricedEntity):
    def __init__(self, currency: Currency, price: float,  name: str = None, discount=None, **kwargs):
        super().__init__(name=name, discount=discount, price=price, currency=currency, **kwargs)
        self.__promo = 0

    def get_price(self):
        return (100 - self.__promo) / 100 * super().get_price()

    def set_promo(self, n: float):
        self.__promo = n

class Cart:
    def __init__(self):
        self.__cart = []

    def get_cart(self):
        return self.__cart

    def index_check(self, index):
        if index > len(self):
            raise IndexError("Товар с таким индексом не найден")

    def __setitem__(self, key, value):
        self.index_check(key)
        self.__cart[key] = value

    def __getitem__(self, index):
        self.index_check(index)
        return self.__cart[index]

    def __add__(self, other):
        if not isinstance(other, Product):
            raise ArithmeticError("К объекту типа Cart можно прибавить только объект типа Product")

        self.__cart.append(other)
        return self

    def __radd__(self, other):
        return self + other

    def __len__(self):
        return len(self.__cart)

    def total(self):
        euros = 0
        rubles = 0
        usds = 0

        for product in self.__cart:
            currency = product.money.currency
            match currency:
                case Currency.Euro:
                    euros += product.get_price()
                case Currency.Ruble:
                    rubles += product.get_price()
                case Currency.USD:
                    usds += product.get_price()

        return {"euro": euros, "ruble": rubles, "usd": usds}


def apply_promotion(cart: Cart, promotion: Promotion):
    match promotion:
        case Promotion.three_for_two:
            for i in range(2, len(cart), 3):
                cart[i].set_promo(100)
        case Promotion.rubles_discount_10:
            for i in range(len(cart)):
                if cart[i].money.currency == Currency.Ruble:
                    cart[i].set_promo(10)

def main():
    p1 = Product(currency=Currency.Ruble, price=100, name="Хлеб")
    p2 = Product(currency=Currency.Ruble, price=200, name="Молоко", discount=10)
    p3 = Product(currency=Currency.Ruble, price=300, name="Сыр")
    p4 = Product(currency=Currency.USD, price=5, name="Газировка")

    cart = Cart()

    cart += p1
    cart += p2
    cart += p3
    cart += p4

    print("Корзина до скидок и акций:")
    for item in cart:
        print(f"{item.get_name()}: {item.get_price()} {item.money.get_currency()}")

    apply_promotion(cart, Promotion.three_for_two)

    print("\nКорзина после акции '3 по цене 2':")
    for item in cart:
        print(f"{item.get_name()}: {item.get_price()} {item.money.get_currency()}")

    apply_promotion(cart, Promotion.rubles_discount_10)

    print("\nКорзина после скидки 10% на рублевые товары:")
    for item in cart:
        print(f"{item.get_name()}: {item.get_price()} {item.money.get_currency()}")

    print(f"\nВсего: {cart.total()}\n")


    m1 = Money(Currency.Ruble, 100)
    m2 = Money(Currency.Ruble, 250)
    m3 = Money(Currency.USD, 5)

    print(f"m1 = {m1.get_currency()} {m1.price}")
    print(f"m2 = {m2.get_currency()} {m2.price}")
    print(f"m3 = {m3.get_currency()} {m3.price}")

    print(f"\nСложение: {m1.get_currency()} {m1.price} + {m2.get_currency()} {m2.price} = {m1 + m2}")

    print(f"Вычитание: {m2.get_currency()} {m2.price} - {m1.get_currency()} {m1.price} = {m2 - m1}")

    print(f"Умножение (скидка 20%): {m1.get_currency()} {m1.price} * 0.2 = {m1 * 0.2}")

    m4 = Money(Currency.Ruble, 100)
    print("\nСравнение денег:")
    print(f"{m1.get_currency()} {m1.price} > {m2.get_currency()} {m2.price}: {m1 > m2}")
    print(f"{m2.get_currency()} {m2.price} > {m1.get_currency()} {m1.price}: {m2 > m1}")
    print(f"{m1.get_currency()} {m1.price} == {m4.get_currency()} {m4.price}: {m1 == m4}")

if __name__ == "__main__":
    main()
from datetime import datetime
from abc import ABC
from money import Money, Currency


class Entity(ABC):
    _id = -1

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        Entity._id += 1
        self._name = name
        self._id = Entity._id
        self._created_at = datetime.now()

    def get_name(self):
        return self._name

class PricedEntity(Entity, ABC):
    def __init__(self, currency: Currency, price: float, **kwargs):
        super().__init__(**kwargs)
        self.__money = Money(currency, price)

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, currency: Currency, price: float):
        self.__money = Money(currency, price)

    def get_price(self):
        return self.money.price

class DiscountableEntity(Entity, ABC):
    def __init__(self, discount, **kwargs):
        super().__init__(**kwargs)
        self._discount = discount

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, discount):
        if discount < 0 or discount > 100:
            raise ValueError("Скидка должна быть больше или равна нулю и не больше ста")

        self._discount = discount

    def get_price(self):
        money = super().money
        if self._discount is None:
            return money

        return Money(money.currency, (100 - self._discount) / 100.0 * money.price)
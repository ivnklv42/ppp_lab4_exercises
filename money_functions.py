def get_currency(obj):
    from money import Money
    return obj.currency

def check_currency(obj1, obj2):
    from money import Money
    if obj1.currency != obj2.currency:
        raise ValueError("Данную операцию можно провести только при одинаковой валюте")

def check_price(price):
    from money import Money
    if price <= 0 or price > 1_000_000_000:
        raise ValueError("Цена должна быть больше нуля и меньше миллиарда")

def is_money(obj):
    from money import Money
    if not isinstance(obj, Money):
        return NotImplemented


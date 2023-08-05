
from .currency import Currency
import math


class Money:
    """
    Class that represents a amount of money of a given currency.
    """

    def __init__(self, currency: Currency, amount: int = 0):
        self.currency = currency
        self.amount = amount

    def __eq__(self, value: "Money"):
        if isinstance(value, Money):
            if value.currency == self.currency and value.amount == self.amount:
                return True
        return False

    def __ne__(self, value: "Money"):
        return not self.__eq__(value)

    def __gt__(self, value: "Money"):
        if isinstance(value, Money):
            if value.currency == self.currency and self.amount > value.amount:
                return True
        return False

    def __ge__(self, value: "Money"):
        if isinstance(value, Money):
            if value.currency == self.currency and self.amount >= value.amount:
                return True
        return False

    def __lt__(self, value):
        return not self.__ge__(value)

    def __le__(self, value):
        return not self.__gt__(value)

    def __str__(self):
        return f"{self.units()}.{self.cents()} {self.currency.code}"

    def __to_amount(self, units: int, cents: int):
        # Handle the case where cents is more than 1 unit.
        if cents > pow(10, self.currency.exponent):
            units += cents // pow(10, self.currency.exponent)
            cents = cents % pow(10, self.currency.exponent)

        return units * pow(10, self.currency.exponent) + cents

    def __is_valid_money(self, value: "Money"):
        if not isinstance(value, Money):
            raise TypeError(f"can't add value of type {type(value)}")

        if self.currency != value.currency:
            raise ValueError(
                f"currency mismatch {self.currency.code} != {self.currency.code}")

    def units(self):
        """
        Gets the amount of money without cents.
        """
        if self.amount >= 0:
            return math.floor(self.amount / pow(10, self.currency.exponent))
        return math.ceil(self.amount / pow(10, self.currency.exponent))

    def cents(self) -> int:
        """
        Gets the amount of cents based on the currency exponent.
        """
        return abs(self.amount) - pow(10, self.currency.exponent) * abs(self.units())

    def to_float(self) -> float:
        if self.amount < 0:
            return -(abs(self.units()) + self.cents() / pow(10, self.currency.exponent))
        return self.units() + self.cents() / pow(10, self.currency.exponent)

    def add(self, units: int, cents: int):
        self.amount += self.__to_amount(units, cents)

    def sub(self, units: int, cents: int):
        self.amount -= self.__to_amount(units, cents)

    def mul(self, times: int):
        self.amount *= times

    def div(self, times: int):
        """
        Divides the current amount.

        Beware as some amount may be lost.

        Here you can lose 1 amount for example:

        5 // 2 == 2
        """

        self.amount //= times

    def __add__(self, value: "Money"):
        self.__is_valid_money(value)

        self.amount += value.amount

        return self

    def __sub__(self, value: "Money"):
        self.__is_valid_money(value)

        self.amount -= value.amount

        return self

    def __mul__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"can't add value of type {type(value)}")

        self.amount *= value

        return self

    def __floordiv__(self, value: int):
        """
        Beware as some amount may be lost.
        """
        if not isinstance(value, int):
            raise TypeError(f"can't add value of type {type(value)}")

        self.amount //= value

        return self

    def __truediv__(self, value: int):
        return self.__floordiv__(value)

    def __pow__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"can't add value of type {type(value)}")

        self.amount **= value

        return self

    def __mod__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"can't add value of type {type(value)}")

        self.amount %= value

        return self

    def __invert__(self):
        self.amount = ~self.amount

        return self

from typing import Optional


class Currency:
    """
    Class that represents a currency.
    """

    def __init__(self, name: str, code: str, numcode: Optional[str], exponent: int):
        self.name = name
        self.code = code
        self.numcode = numcode
        self.exponent = exponent

    def __eq__(self, value: "Currency"):
        if isinstance(value, Currency):
            if value.code == self.code:
                return True

        return False

    def __str__(self):
        return self.name

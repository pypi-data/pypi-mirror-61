# money.py
[![PyPI version](https://badge.fury.io/py/money.py.svg)](https://badge.fury.io/py/money.py)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fcryptgar%2Fmoney.py%2Fbadge&style=flat)](https://actions-badge.atrox.dev/cryptgar/money.py/goto)

> money.py is a library to handle money

*Python 3.6+ only.*

https://en.wikipedia.org/wiki/ISO_4217

## Documentation

Will make it ASAP.

## Installation

- ``pip3 install money.py``

### Testing

- `pip install pytest pytest-cov pytest-xdist`

- `pytest --cov=moneypy`

## Example

```python
from moneypy import Money, EUR_CURRENCY

a = Money(EUR_CURRENCY)
b = Money(EUR_CURRENCY)

a.add(2, 30) # 2.30
b.add(4, 4) # 4.4

a += b
print(a) # 6.7
```

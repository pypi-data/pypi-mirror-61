# money.py

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
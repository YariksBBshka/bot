
from currency_converter import CurrencyConverter
from decimal import Decimal
c = CurrencyConverter()
def converter_to_RUB(cur,n):
    if cur=="₽":
        return round((n), 2)
    if cur=="$":
        return round((n/(c.convert(1, 'RUB', 'USD'))), 2)
    if cur=="€":
        return round((n/(c.convert(1, 'RUB', 'EUR'))), 2)

# def convert_from_RUB_to_EUR(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'RUB', 'EUR'))
#     output_currency = round(x, 2)
#     return output_currency
# def convert_from_RUB_to_USD(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'RUB', 'USD'))
#     output_currency = round(x, 2)
#     return output_currency
# def convert_from_EUR_to_RUB(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'EUR', 'PHP'))
#     output_currency = round(x, 2)
#     return output_currency
# def convert_from_USD_to_RUB(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'USD', 'PHP'))
#     output_currency = round(x, 2)
#     return output_currency
# def convert_from_USD_to_EUR(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'USD', 'EUR'))
#     output_currency = round(x, 2)
#     return output_currency
# def convert_from_EUR_to_USD(n):
#     c = CurrencyConverter()
#     x = Decimal(c.convert(n, 'EUR', 'USD'))
#     output_currency = round(x, 2)
#     return output_currency
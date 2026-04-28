from utils.utilities import *


def get_currency_code(country):
    for key,value in country_to_currency.items():
        if (country==key):
            return value

# print(get_currency_code("India"))
import json

import requests

from constants import *


def returnReqError(url, result):
    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    print(f"JSON result type: {type(result.json())}")
    print(result.json())


def get_exchange_rates(base = None, symbol = None):
    url = EXCHANGE_RATES_API_URL + "/latest"
    if base is not None:
        url += "?base=" + base.upper()
    if symbol is not None:
        if base is not None:
            url += "&"
        else:
            url += "?"
        url += "symbols=" + symbol.upper()

    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return False

    return result.json()["rates"]


def valid_fiat(symbol):
    symbol = symbol.upper()

    exchange_rates = get_exchange_rates(symbol = symbol, base = "USD")

    if exchange_rates is False:
        return False

    for keyval in exchange_rates:
        if symbol == keyval:
            return True

    return False
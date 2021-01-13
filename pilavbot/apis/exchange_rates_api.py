import json

import requests

from constants import *


def returnReqError(url, result):
    """Handler for the request errors

    Args:
        url (str): URL which the request was made
        result (requests.models.Response): Response of the request
    """

    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    print(f"JSON result type: {type(result.json())}")
    print(result.json())


def get_exchange_rates(base=None, symbol=None):
    """Get exchange rates using given base and symbol.

    Args:
        base (str, optional): Symbol representation of the fiat which will be used as the base(eg. USD for United States Dollar). Defaults to None.
            API returns using USD base if None.
        symbol (str, optional): Symbol representation of the fiat (eg. USD for United States Dollar). Defaults to None.
            API returns all available fiats if None.

    Returns:
        List: A list which consists of json-encoded exchange rates list.
    """

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
        return None

    return result.json()["rates"]


def valid_fiat(symbol):
    """Checks if the fiat is valid or not.

    Args:
        symbol (str): Symbol representation of the fiat (eg. USD for United States Dollar).

    Returns:
        bool: If the fiat exists or not.
    """

    symbol = symbol.upper()

    exchange_rates = get_exchange_rates(symbol=symbol, base="USD")

    if exchange_rates is None:
        return False

    for keyval in exchange_rates:
        if symbol == keyval:
            return True

    return False

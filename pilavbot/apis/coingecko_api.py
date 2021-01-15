import json

import requests

from constants import *


def returnReqError(url, result):
    """Handler for the request errors.

    Args:
        url (str): URL which the request was made.
        result (requests.models.Response): Response of the request.
    """

    print("Request error!")
    print(f"Url: {url}")
    print(f"Status Code: {result.status_code}")
    print(f"JSON result type: {type(result.json())}")
    print(result.json())


def get_coins_list():
    """Get the list of all coins.

    Returns:
        List: A list which consists of json-encoded coins list.
    """

    url = COINGECKO_API_URL + "/coins/list"
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    return result.json()


def valid_coin(symbol):
    """Checks if the coin is valid or not.

    Args:
        symbol (str): Symbol representation of the coin (eg. BTC for Bitcoin).

    Returns:
        bool: If the coin exists or not.
    """

    symbol = symbol.lower()

    coins = get_coins_list()
    if coins is None:
        return False

    for keyval in coins:
        if symbol == keyval["symbol"].lower():
            return True
    return False


def get_id_from_symbol(symbol):
    """Get id of coin using its symbol representation.

    Args:
        symbol (str): Symbol representation of the coin (eg. BTC for Bitcoin).

    Returns:
        str: Id of the coin.
    """
    symbol = symbol.lower()

    coins = get_coins_list()
    if coins is False:
        return None

    for keyval in coins:
        if symbol == keyval["symbol"].lower():
            return keyval["id"]
    return None


def get_price_data(symbol):
    """Get price data of the given coin.

    Args:
        symbol (str): Symbol representation of the coin (eg. BTC for Bitcoin).

    Returns:
        dict: A dict which consists of following keys:
            current_price, high_24h, low_24h, price_change_percentage_24h, price_change_percentage_7d and price_change_percentage_30d, market_cap_rank.
    """

    id = get_id_from_symbol(symbol)
    if id is None:
        return None

    url = COINGECKO_API_URL + "/coins/" + id
    result = requests.get(url)
    if result.status_code != 200:
        returnReqError(url, result)
        return None

    result = result.json()["market_data"]
    return {
        "current_price": result["current_price"]["usd"],
        "high_24h": result["high_24h"]["usd"],
        "low_24h": result["low_24h"]["usd"],
        "price_change_percentage_24h": result["price_change_percentage_24h"],
        "price_change_percentage_7d": result["price_change_percentage_7d"],
        "price_change_percentage_30d": result["price_change_percentage_30d"],
        "market_cap_rank": result["market_cap_rank"],
    }

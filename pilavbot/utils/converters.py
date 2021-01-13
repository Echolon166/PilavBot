import re

from discord.ext import commands

import errors
from apis import coingecko_api, exchange_rates_api


class UnicodeEmoji(commands.Converter):
    """Converter to check if the emoji is an unicode emoji.

        Raises:
            errors.EmojiNotFound: Given emoji is not an unicode emoji.

        Returns:
            str: String representation of the emoji.
    """

    async def convert(self, ctx, argument):
        pattern = re.compile(
            "(["
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "])"
        )

        valid = re.match(pattern, argument)
        if not valid:
            raise errors.EmojiNotFound

        return argument


class CryptoCoin(commands.Converter):
    """Converter to check if the given coin is valid, and if valid, return it's price data.

        Raises:
            errors.InvalidSymbol: No coin exists with given symbol.
            errors.RequestError: There was an error while fetching the data.

        Returns:
            dict: A dict which consists of following keys:
                symbol and data(price data).
    """

    async def convert(self, ctx, argument):
        # Check if the coin is valid
        valid = coingecko_api.valid_coin(argument)
        if not valid:
            raise errors.InvalidSymbol("Invalid coin symbol")

        # Retrieve the price data of the coin
        data = coingecko_api.get_price_data(argument)
        if data is None:
            raise errors.RequestError(
                "There was an error while fetching the coin data")

        return {"symbol": argument, "data": data}


class Fiat(commands.Converter):
    """Converter to check if the given fiat is valid

        Raises:
            errors.InvalidSymbol: No fiat exists with given symbol.

        Returns:
            str: Symbol of the fiat.
    """

    async def convert(self, ctx, argument):
        # Check if the fiat is valid
        valid = exchange_rates_api.valid_fiat(argument)
        if not valid:
            raise errors.InvalidSymbol("Invalid fiat symbol")

        return argument

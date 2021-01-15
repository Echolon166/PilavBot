import sys
import traceback
from typing import Optional

import discord
from discord.ext import commands
from discord.utils import get

import errors
from utils import pretty_print
from utils.converters import CryptoCoin, Fiat, Location
from apis import exchange_rates_api
from constants import *


class InfoCommands(commands.Cog):
    """Cog for processing commands which return info about something.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_after_invoke(self, ctx):
        """A special method that is called whenever an command is called inside this cog.
        """

        """
        await pretty_print(
            ctx, 
            "Command completed successfully!", 
            title="Success", 
            color=SUCCESS_COLOR,
        )
        """
        pass

    @errors.standard_error_handler
    async def cog_command_error(self, ctx, error):
        """A special method that is called whenever an error is dispatched inside this cog.
            This is similar to on_command_error() except only applying to the commands inside this cog.

        Args:
            ctx (Context) – The invocation context where the error happened.
            error (CommandError) – The error that happened.
        """

        print(
            "Ignoring exception in command {}:".format(ctx.command),
            file=sys.stderr,
        )
        traceback.print_exception(
            type(error),
            error,
            error.__traceback__,
            file=sys.stderr,
        )

    @commands.command(
        name="weather",
        help="Get current weather of a location"
    )
    async def weather(self, ctx, *, location: Location):
        location_name = location["location_name"]
        data = location["data"]

        await pretty_print(
            ctx,
            [
                {
                    "name": "Descripition",
                    "value": f"{data['weather_description']}",
                    "inline": False,
                },
                {
                    "name": "Temperature(°C)",
                    "value": f"{data['temp']}°",
                    "inline": False,
                },
                {
                    "name": f"***Feels Like***",
                    "value": f"{data['temp_feels_like']}°",
                },
                {
                    "name": f"***Max.***",
                    "value": f"{data['temp_max']}°",
                },
                {
                    "name": f"***Min.***",
                    "value": f"{data['temp_min']}°",
                },
                {
                    "name": "Humidity(%)",
                    "value": f"{data['humidity']}%",
                },
                {
                    "name": "Wind",
                    "value": f"{data['wind_speed']} km/h",
                },
            ],
            thumbnail=data["icon_url"],
            title=f"Weather in {location_name}, {data['location_country']}",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="exchange_rate",
        aliases=["exrate"],
        help="Get the exchange rate of a fiat currency"
    )
    async def exchange_rate(self, ctx, symbol: Fiat, base: Optional[Fiat]):
        base = base or "USD"
        rate = exchange_rates_api.get_exchange_rates(symbol=symbol, base=base)

        await pretty_print(
            ctx,
            [
                {
                    "name": f"{base}/{symbol}",
                    "value": f"1 {base} = {'%.2f' % round(rate[symbol], 2)} {symbol}",
                },
            ],
            title="Exchange Rate",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    @commands.command(
        name="crypto_price",
        aliases=["cprice"],
        help="Get the price of a crypto coin"
    )
    async def crypto_price(self, ctx, coin: CryptoCoin):
        data = coin["data"]

        price_change_perc_24h = data["price_change_percentage_24h"]
        price_change_perc_7d = data["price_change_percentage_7d"]
        price_change_perc_30d = data["price_change_percentage_30d"]

        # Add + in front of the positive percentages to show green color (- comes from api itself for negatives)
        if price_change_perc_24h >= 0:
            price_change_perc_24h = "+" + str(price_change_perc_24h)
        if price_change_perc_7d >= 0:
            price_change_perc_7d = "+" + str(price_change_perc_7d)
        if price_change_perc_30d >= 0:
            price_change_perc_30d = "+" + str(price_change_perc_30d)

        await pretty_print(
            ctx,
            [
                {
                    "name": "Current Price",
                    "value": f"```diff\n${data['current_price']}```",
                    "inline": False,
                },
                {
                    "name": "24h Price Change",
                    "value": f"```diff\n{price_change_perc_24h}%\n```",
                },
                {
                    "name": "7d Price Change",
                    "value": f"```diff\n{price_change_perc_7d}%```",
                },
                {
                    "name": "30d Price Change",
                    "value": f"```diff\n{price_change_perc_30d}%```",
                },
                {
                    "name": "24h Low",
                    "value": f"```diff\n{data['low_24h']}```",
                },
                {
                    "name": "24h High",
                    "value": f"```diff\n{data['high_24h']}```",
                },
                {
                    "name": "Market Cap Rank",
                    "value": f"```diff\n{data['market_cap_rank']}```",
                },
            ],
            title=f"{coin['symbol']} Price Statistics",
            footer=self._requested_by_footer(ctx),
            timestamp=True,
            color=WHITE_COLOR,
        )

    def _requested_by_footer(self, ctx):
        # Return empty dict if in private message
        if ctx.guild is None:
            return {}

        # Return requested by author message and author avatar url if in guild
        return {
            "text": f"Requested by {ctx.author.name}",
            "icon_url": ctx.author.avatar_url,
        }

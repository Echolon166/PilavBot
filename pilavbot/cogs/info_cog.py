import sys
import traceback
from typing import Optional

import discord
from discord.ext import commands
from discord.utils import get
from discord import Color

import errors
from utils import pretty_print, gradient
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
            footer={
                "text": f"Requested by {ctx.author.name}",
                "icon_url": ctx.author.avatar_url,
            },
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
            f"1 {base} = {'%.2f' % round(rate[symbol], 2)} {symbol}",
            title=f"Exchange Rate of {base}/{symbol}",
            color=WHITE_COLOR,
        )

    @commands.command(
        name="crypto_price",
        aliases=["cprice"],
        help="Get the price of a crypto coin"
    )
    async def crypto_price(self, ctx, coin: CryptoCoin):

        # Gets gradient color which will represent the change in price.
        def get_gradient_color(percentage):
            percentage = 50 + int(percentage) / 2
            return gradient(
                Color.red(),
                Color.magenta(),
                Color.lighter_grey(),
                Color.teal(),
                Color.green(),
                percentage=percentage,
            )

        data = coin["data"]

        percentage_24h = data["price_change_percentage_24h"]
        percentage_30d = data["price_change_percentage_30d"]

        await pretty_print(
            ctx,
            f"${data['current_price']}",
            title=f"Price of {coin['symbol']}",
            color=WHITE_COLOR,
        )
        await pretty_print(
            ctx,
            f"{percentage_24h}%",
            title="24H Price Change",
            color=get_gradient_color(percentage_24h),
        )
        await pretty_print(
            ctx,
            f"{percentage_30d}%",
            title="30D Price Change",
            color=get_gradient_color(percentage_30d),
        )

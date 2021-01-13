import sys
import traceback
import os

import discord
from discord.ext import commands
from discord.utils import get

import data
import errors
import validation
from constants import *
from utils import pretty_print


class SetupCommands(commands.Cog):
    """Cog for processing setup commands which are often only represented only to administrators.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_after_invoke(self, ctx):
        """A special method that is called whenever an command is called inside this cog.
        """

        await pretty_print(
            ctx,
            "Command completed successfully!",
            title="Success",
            color=SUCCESS_COLOR,
        )

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
        name="add_root_required_emojis",
        help="Adds required emojis for root setup command to the server",
    )
    @validation.owner_or_permissions(administrator=True)
    @validation.missing_required_assets(ROOT_EMOJI_PATH)
    async def add_root_required_emojis(self, ctx):
        asset_path = ROOT_EMOJI_PATH

        for asset in os.listdir(asset_path):
            asset_name = asset.split(".")[0]
            # Gets the emoji from the guild(If it exists).
            emoji = get(ctx.message.guild.emojis, name=asset_name)
            # If emoji doesn't exists in the guild, add it.
            if not emoji:
                with open(f"{asset_path}/{asset}", "rb") as img:
                    img_byte = img.read()
                    await ctx.guild.create_custom_emoji(
                        name=asset_name,
                        image=img_byte,
                    )

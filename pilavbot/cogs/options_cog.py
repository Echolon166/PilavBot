import sys
import traceback
from typing import Union

import discord
from discord.ext import commands

import data
import errors
import validation
from constants import *

from utils import pretty_print
from utils.converters import UnicodeEmoji


class OptionsCommands(commands.Cog):  
    """
    Cog for processing options commands.
    """


    def __init__(self, bot):
        self.bot = bot


    async def cog_after_invoke(self, ctx):
        await pretty_print(
            ctx, "Command completed successfully!", title="Success", color=SUCCESS_COLOR
        )
        pass


    @errors.standard_error_handler
    async def cog_command_error(self, ctx, error):
        """
        A special method that is called whenever an error is dispatched inside this cog.
        This is similar to on_command_error() except only applying to the commands inside this cog.

        Parameters
        __________

          ctx (Context) – The invocation context where the error happened.
          error (CommandError) – The error that happened.

        """

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )


    @commands.command(
        name="set_prefix",
        help=" <prefix> Prefix for bot commands",
    )
    @validation.owner_or_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        data.add_prefix_mapping(ctx.guild.id, prefix)

    
    @commands.command(
        name="set_join_emoji", 
        help=" <emoji> Change the join emoji for various commands",
    )
    @validation.owner_or_permissions(administrator=True)
    async def set_join_emoji(self, ctx, emoji: Union[commands.EmojiConverter, UnicodeEmoji]):
        data.set_join_emoji(ctx.guild.id, str(emoji))

    
    @commands.command(
        name="set_start_emoji", 
        help=" <emoji> Change the start emoji for various commands",
    )
    @validation.owner_or_permissions(administrator=True)
    async def set_start_emoji(self, ctx, emoji: Union[commands.EmojiConverter, UnicodeEmoji]):
        data.set_start_emoji(ctx.guild.id, str(emoji))
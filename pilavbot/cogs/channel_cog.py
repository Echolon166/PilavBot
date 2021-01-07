import sys
import traceback

import discord
from discord.ext import commands

import data
import errors
import validation
from constants import *

from utils import pretty_print


class ChannelCommands(commands.Cog):  
    """
    Cog for processing commands from a specific channel.
    """


    def __init__(self, bot):
        self.bot = bot


    async def cog_after_invoke(self, ctx):
        """await pretty_print(
            ctx, "Command completed successfully!", title="Success", color=SUCCESS_COLOR
        )"""
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
        name="root_setup", 
        help="Setup a new root game"
    )
    @commands.guild_only()
    async def root_setup(self, ctx):
        start_emoji = data.get_start_emoji(ctx.guild.id) or DEFAULT_START_EMOJI_STR
        join_emoji = data.get_join_emoji(ctx.guild.id) or DEFAULT_JOIN_EMOJI_STR

        setup_message = await pretty_print(
            ctx,
            f"The author should add {start_emoji} to start.\n\nPlease add {join_emoji} as a reaction if you want to join.",
            title="Setting up a new root game!",
            color=SUCCESS_COLOR,
        )
        await setup_message.add_reaction(emoji=join_emoji)
        await setup_message.add_reaction(emoji=start_emoji)

        while(True):
            reaction = await self.bot.wait_for('reaction_add', check=lambda reaction, author: author == ctx.author)

            if(str(reaction[0].emoji) == start_emoji and reaction[0].message.id == setup_message.id):
                break

        msg = await ctx.fetch_message(setup_message.id)

        users = []
        for reaction in msg.reactions:
            if str(reaction) == join_emoji:
                async for user in reaction.users():
                    if user.bot != True:
                        users.append(user)
                break

        await setup_message.delete()
        
        await pretty_print(
            ctx,
            f"{', '.join(user.name for user in users)}",
            title="Players",
            color=SUCCESS_COLOR,
        )
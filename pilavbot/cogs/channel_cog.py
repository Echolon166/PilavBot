import sys
import traceback
import os
import random
import math
import time
import asyncio

import discord
from discord import Color
from discord.ext import commands
from discord.utils import get
from utils.converters import CryptoCoin

import data
import errors
import validation
from utils import pretty_print, gradient
from constants import *


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


    @commands.command(name="price", help="Get the price data of a crypto coin.")
    async def price(self, ctx, coin: CryptoCoin):


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

        if not data:
            raise errors.RequestError("There was an error while fetching the coin data")
        else:
            await pretty_print(
                ctx,
                f"{data['current_price']}",
                title=f"Current Price of {coin['symbol']}",
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


    @commands.command(
        name="suicide",
        help="Commit sudoku"
    )
    @commands.guild_only()
    async def suicide(self, ctx):
        try:
            await ctx.send(f"{ctx.author} committed sudoku.")
            await ctx.guild.kick(ctx.author)
        except discord.Forbidden:
            await ctx.send("I'm not strong enough to kill you, yet.")


    @commands.command(
        name="russian_roulette",
        help="<magazine> <bullet> Start a new russian roulette game"
    )
    @commands.guild_only()
    async def russian_roulette(self, ctx, magazine = 6, bullets = 1):


        async def shoot(user):
            if next(revolver_iter) == 1:
                try:
                    await ctx.guild.kick(user)
                    await ctx.send(f"{user.mention} died.")
                except discord.Forbidden:
                    await ctx.send(f"{user.mention} cheated death and is still alive, but if there's one thing for sure, it's that he lost.")
                nonlocal bullets
                bullets -= 1
            else:
                await ctx.send(f"{user.mention} shot but he is still alive.")

        
        def load_revolver(self, ctx, magazine, bullets):
            revolver = [0 for i in range(magazine)]

            while(bullets):
                slot = random.randint(0, magazine - 1)
                if revolver[slot] != 1:
                    evolver[slot] = 1
                    bullets -= 1

            return revolver


        revolver = load_revolver(magazine, bullets)
        users = await self._get_setup_participants(ctx, "russian roulette")

        await ctx.send('*Gun is initialized*')
        time.sleep(WAIT_TIME)
        await ctx.send('*Gun is Loaded*')
        time.sleep(WAIT_TIME)
        await ctx.send('*Chamber is spun*')
        time.sleep(WAIT_TIME)

        self.load_revolver(ctx, magazine, bullets)

        revolver_iter = iter(revolver)
        user_iter = iter(users)
        while(bullets > 0):
            if iter(user_iter).__length_hint__() == 0:
                user_iter = iter(users)

            user = next(user_iter)
            
            def check(message):
                return message.author == user and str(message.content) == f"shoot"

            shoot_message = await ctx.send(f"{user.mention}, it's your turn to shoot. You should type shoot to shoot. (You have 10 seconds.)")

            try:
                await self.bot.wait_for('message', check=check, timeout = 10.0)
                await shoot(user)
            except asyncio.TimeoutError:
                await ctx.send(f"{user.mention} had no guts to shoot himself, so he is being forced to do so.")
                await shoot(user)
            await shoot_message.delete()

            time.sleep(WAIT_TIME)

        await ctx.send(f"The magazine is empty, so the roulette is over. Congratulations to triumphant survivors.")


    @commands.command(
        name="root_setup", 
        help="Setup a new root game"
    )
    @commands.guild_only()
    async def root_setup(self, ctx):


        def get_faction_emojis(self, ctx):
            required_assets = os.listdir(ROOT_EMOJI_PATH)

            faction_emojis = {}
            for asset in required_assets:
                asset_name = asset.split(".")[0]
                faction_emojis[asset_name] = get(ctx.message.guild.emojis, name=asset_name)
                if faction_emojis[asset_name] is None:
                    raise errors.MissingRequiredAssets("Please add all required emojis to the server first.\nAn admin can call 'add_root_required_emojis' to do so.")
        
            return faction_emojis


        def check(reaction, author):
                return author == user and reaction.message.id == pick_message.id
                

        faction_names_by_tag = {
            "faction_marquise": "Marquise de Cat",
            "faction_eyrie": "Eyrie Dynasties",
            "faction_vagabond": "Vagabond",
            "faction_riverfolk": "Riverfolk Company",
            "faction_alliance": "Woodland Alliance",
            "faction_cult": "Lizard Cult",
        }
        available_factions = {
            "faction_marquise": 10, 
            "faction_eyrie": 7, 
            "faction_vagabond": 5, 
            "faction_riverfolk": 5, 
            "faction_alliance": 3, 
            "faction_cult": 2,
        }
        faction_emojis = self.get_faction_emojis(ctx)

        users = await self._get_setup_participants(ctx, "root", 6)
        random.shuffle(users)

        user_factions = []
        players_to_pick = len(users)
        pick_messages = []

        required_reach = 17
        for i in range(2, len(users)): 
            ex = math.floor((i - 1) / 2)
            required_reach += (i - 1) + (-1)**(ex+1) + 0**ex

        for user in users:
            test_reach = 0
            for i in range(players_to_pick):
                if i != players_to_pick - 1:
                    test_reach += available_factions[list(available_factions.keys())[i]]
                else:
                    while True:
                        test_reach = test_reach
                        test_reach += available_factions[list(available_factions.keys())[-1]]
                        if test_reach >= required_reach:
                            break
                        available_factions.pop(list(available_factions.keys())[-1])

            if len(available_factions) == 1:
                user_factions.append(list(available_factions.keys())[0])
                await ctx.send(f"{user.mention}, since there is only one available faction left to pick, you've been assigned to it automatically.")
            else:
                pick_message = await ctx.send(f"{user.mention}, it's your turn to pick. Please pick your faction from the reactions of this message.")
                for faction in available_factions:
                    await pick_message.add_reaction(emoji=faction_emojis[faction])

                while True:
                    reaction, author = await self.bot.wait_for('reaction_add', check=check)
                    emoji = str(reaction.emoji).split(":")[1]
                    if emoji in available_factions:
                        required_reach -= available_factions[emoji]
                        user_factions.append(emoji)

                        if emoji == "faction_vagabond" and available_factions["faction_vagabond"] != 2:
                            available_factions.pop(emoji)
                            available_factions["faction_vagabond"] = 2
                        else:
                            available_factions.pop(emoji)

                        break

                pick_messages.append(pick_message)

            players_to_pick -= 1

        user_picks_str = ""
        faction_iter = iter(user_factions)
        for user in users:
            user_picks_str += f"{user.display_name}: {faction_names_by_tag[next(faction_iter)]}\n"

        await pretty_print(
            ctx,
            user_picks_str,
            title="Player Factions",
            color=SUCCESS_COLOR,
        )

        time.sleep(WAIT_TIME * 2)
        for message in pick_messages:
            await message.delete()


    async def _get_setup_participants(self, ctx, game_name, max_player = 99999):
        start_emoji = data.get_start_emoji(ctx.guild.id) or DEFAULT_START_EMOJI_STR
        join_emoji = data.get_join_emoji(ctx.guild.id) or DEFAULT_JOIN_EMOJI_STR

        setup_message = await pretty_print(
            ctx,
            f"The author should add {start_emoji} to start.\n\nPlease add {join_emoji} as a reaction if you want to join.",
            title=f"Setting up a new {game_name} game!",
            color=SUCCESS_COLOR,
        )
        await setup_message.add_reaction(emoji=join_emoji)
        await setup_message.add_reaction(emoji=start_emoji)

        while(True):
            reaction, author = await self.bot.wait_for('reaction_add')

            if(str(reaction.emoji) == start_emoji and 
                reaction.message.id == setup_message.id and 
                author == ctx.author):
                    break

            if(str(reaction.emoji) == join_emoji and
                reaction.message.id == setup_message.id and
                reaction.count >= max_player + 1):
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

        if len(users) < 2:
            raise errors.NotEnoughParticipants("At least 2 participants required to start the setup.")

        return users
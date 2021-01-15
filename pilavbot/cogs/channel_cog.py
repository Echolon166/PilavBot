import sys
import traceback
import os
import random
import math
import time
import asyncio

import discord
from discord.ext import commands
from discord.utils import get

import data
import errors
from utils import pretty_print
from constants import *


class ChannelCommands(commands.Cog):
    """Cog for processing commands from a specific channel.
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
        name="suicide",
        help="Commit sudoku"
    )
    @commands.guild_only()
    async def suicide(self, ctx):
        try:
            await ctx.guild.kick(ctx.author)
            await ctx.send(f"{ctx.author.mention} committed sudoku.")
        # Bot has no permission to kick the user
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention} tried to commit sudoku.")
            await ctx.send("I'm not strong enough to kill you, yet.")

    @commands.command(
        name="russian_roulette",
        help="Start a new russian roulette game"
    )
    @commands.guild_only()
    async def russian_roulette(self, ctx, magazine: int = 6, bullets: int = 1):

        # Shoot the user, if there is a bullet(1) in revolver_iter, kick the user
        async def shoot(user):
            if next(revolver_iter) == 1:
                try:
                    await ctx.guild.kick(user)
                    await ctx.send(f"{user.mention} died.")
                # Bot has no permission to kick the user
                except discord.Forbidden:
                    await ctx.send(f"{user.mention} cheated death and is still alive, but if there's one thing for sure, it's that he lost.")
                nonlocal bullets
                bullets -= 1
            else:
                await ctx.send(f"{user.mention} shot but he is still alive.")

        def load_revolver():
            mag = magazine
            bul = bullets
            revolver = [0 for i in range(mag)]

            while(bul):
                slot = random.randint(0, mag - 1)
                if revolver[slot] != 1:
                    revolver[slot] = 1
                    bul -= 1

            return revolver

        # Load revolver with given amount of bullets
        revolver = load_revolver()
        # Get participants
        users = await self._get_participants(
            ctx,
            "russian roulette",
            min_participant=1,
        )

        await ctx.send('*Gun is initialized*')
        time.sleep(WAIT_TIME)
        await ctx.send('*Gun is Loaded*')
        time.sleep(WAIT_TIME)
        await ctx.send('*Chamber is spun*')
        time.sleep(WAIT_TIME)

        revolver_iter = iter(revolver)
        user_iter = iter(users)
        # As long as bullet count is above 0, iterate through the participants
        while(bullets > 0):
            if iter(user_iter).__length_hint__() == 0:
                user_iter = iter(users)

            user = next(user_iter)

            def check(message):
                return message.author == user and str(message.content) == f"shoot"

            # Ask current participant to shoot
            shoot_message = await ctx.send(f"{user.mention}, it's your turn to shoot. You should type shoot to shoot. (You have 10 seconds.)")

            # Wait till timeout for users message, and if timeout reaches, shoot the user regardless of his message
            try:
                t_message = await self.bot.wait_for('message', check=check, timeout=10.0)
                await shoot(user)
            except asyncio.TimeoutError:
                t_message = await ctx.send(f"{user.mention} had no guts to shoot himself, so he is being forced to do so.")
                await shoot(user)
            await shoot_message.delete()

            await t_message.delete()
            time.sleep(WAIT_TIME)

        await ctx.send(f"The magazine is empty, so the roulette is over. Congratulations to triumphant survivors.")

    @commands.command(
        name="root_setup",
        help="Setup a new root game"
    )
    @commands.guild_only()
    async def root_setup(self, ctx):

        def get_faction_emojis(self):
            # Get required asset list from root emoji path
            required_assets = os.listdir(ROOT_EMOJI_PATH)

            faction_emojis = {}
            # Get assets from the guild, raise error if any of them is missing
            for asset in required_assets:
                asset_name = asset.split(".")[0]
                faction_emojis[asset_name] = get(
                    ctx.message.guild.emojis,
                    name=asset_name,
                )
                if faction_emojis[asset_name] is None:
                    raise errors.MissingRequiredAssets(
                        "Please add all required emojis to the server first.\nAn admin can call 'add_root_required_emojis' to do so.")

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
        faction_emojis = get_faction_emojis(ctx)

        # Get participants
        users = await self._get_participants(
            ctx,
            "root",
            max_participant=6,
            min_participant=2,
        )
        random.shuffle(users)

        user_factions = []
        players_to_pick = len(users)
        pick_messages = []

        # Calculate required reach
        required_reach = 17
        for i in range(2, len(users)):
            ex = math.floor((i - 1) / 2)
            required_reach += (i - 1) + (-1)**(ex+1) + 0**ex

        # Each user picks their faction
        for user in users:
            test_reach = 0
            # Calculate test reach for possible factions
            for i in range(players_to_pick):
                if i != players_to_pick - 1:
                    test_reach += available_factions[list(
                        available_factions.keys())[i]]
                else:
                    # If test reach doesn't reach required reach, remove the faction with lowest reach and
                    #   calculate again with new lowest one
                    while True:
                        last_reach = available_factions[list(
                            available_factions.keys())[-1]]
                        test_reach += last_reach
                        if test_reach >= required_reach:
                            break
                        test_reach -= last_reach
                        available_factions.pop(
                            list(available_factions.keys())[-1])

            # If only one faction is available, assign it to remaining user
            if len(available_factions) == 1:
                user_factions.append(list(available_factions.keys())[0])
                await ctx.send(f"{user.mention}, since there is only one available faction left to pick, you've been assigned to it automatically.")
            # If there is more than one available faction, query user to pick one
            else:
                pick_message = await ctx.send(f"{user.mention}, it's your turn to pick. Please pick your faction from the reactions of this message.")
                # Add available faction emojis as reaction to query message, so user can simply choose one of them
                for faction in available_factions:
                    await pick_message.add_reaction(emoji=faction_emojis[faction])

                # Wait until user adds one of the available faction's emoji as reaction to message
                while True:
                    reaction, author = await self.bot.wait_for('reaction_add', check=check)
                    emoji = str(reaction.emoji).split(":")[1]
                    if emoji in available_factions:
                        required_reach -= available_factions[emoji]
                        user_factions.append(emoji)

                        # If vagabond gets picked for the first time, decrease it's reach to 2 for second vagabond
                        if emoji == "faction_vagabond" and available_factions["faction_vagabond"] != 2:
                            available_factions.pop(emoji)
                            available_factions["faction_vagabond"] = 2
                        # If vagabonds gets picked twice or if any other faction gets picked, remove it from available factions
                        else:
                            available_factions.pop(emoji)

                        break

                # Add query message to pick_messages list to delete them later
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

    async def _get_participants(self, ctx, game_name, max_participant=99999, min_participant=0):
        """Get participants by counting the reactions of invitation.

        Args:
            game_name (str): Name of the game to gather participants to.
            max_participant (int, optional): Max participant count. Defaults to 99999.
            min_participant (int, optional): Min participant count. Default to 0.

        Raises:
            errors.NotEnoughParticipants: Participant count doesn't reach the min participant count.

        Returns:
            list(discord.User): List of participants.
        """

        start_emoji = data.get_start_emoji(
            ctx.guild.id) or DEFAULT_START_EMOJI_STR
        join_emoji = data.get_join_emoji(
            ctx.guild.id) or DEFAULT_JOIN_EMOJI_STR

        setup_message = await pretty_print(
            ctx,
            f"The author should add {start_emoji} to start.\n\nPlease add {join_emoji} as a reaction if you want to join.",
            title=f"Setting up a new {game_name} game!",
            color=SUCCESS_COLOR,
        )
        await setup_message.add_reaction(emoji=join_emoji)
        await setup_message.add_reaction(emoji=start_emoji)

        # Loop and listen to reactions until certain requirements are met
        while(True):
            reaction, author = await self.bot.wait_for('reaction_add')

            # If author adds start_emoji, break the loop
            if(str(reaction.emoji) == start_emoji and
                    reaction.message.id == setup_message.id and
                    author == ctx.author):
                break

            # If participant count reaches the max_participant count, break the loop
            if(str(reaction.emoji) == join_emoji and
                    reaction.message.id == setup_message.id and
                    reaction.count >= max_participant + 1):
                break

        msg = await ctx.fetch_message(setup_message.id)

        users = []
        # Get the participants which reacted with join_emoji to message
        for reaction in msg.reactions:
            if str(reaction) == join_emoji:
                async for user in reaction.users():
                    if user.bot != True:
                        users.append(user)
                break

        await setup_message.delete()

        # Check if participant count reaches the min participant count
        if len(users) < min_participant:
            raise errors.NotEnoughParticipants(
                f"At least {min_participant} participants required to start.")

        return users

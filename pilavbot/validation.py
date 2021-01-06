from discord.ext import commands
from discord.utils import get

import errors
import data

def owner_or_permissions(**perms):
    """
    Decorator to check for discord.py specific paramaters before running a given cog command

    Returns
    --------
        True if the user is the owner of the guild or
        the user satisfies all keyword arguments (ex. adminstrator = True)
        and the command is run in a server (Not a private message)

    Raises
    ---------

        CheckFailure
        NoPrivateMessage
    """
    original = commands.has_permissions(**perms).predicate

    async def extended_check(ctx):
        if ctx.guild is None:
            raise errors.NoPrivateMessage
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)

    return commands.check(extended_check)
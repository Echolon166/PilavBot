from discord.ext import commands
import functools

import dataset
import config


def create_dm(cog_function):
    """
    Decorator that creates a Direct Message (dm) and appends it to the current context.
    Must recieve a class function with a Context argument.
    Useful in discord.Cog calls
    """

    # Preserve function name so discord can still call the command
    @functools.wraps(cog_function)
    async def wrapper(cls, ctx, *args, **kwargs):
        ctx.dm = None
        try:
            ctx.dm = await ctx.author.create_dm()
        except:
            print("Could not create dm")
        await cog_function(cls, ctx, *args, **kwargs)

    return wrapper


def send_to_dm(cog_function):
    """
    Decorator that creates a Direct Message (dm) and converts the current context to it
    Must recieve a class function with a Context argument.
    Useful in discord.Cog calls
    """

    # Preserve function name so discord can still call the command
    @functools.wraps(cog_function)
    async def wrapper(cls, ctx, *args, **kwargs):
        try:
            ctx.channel = await ctx.author.create_dm()
        except:
            print("Could not create dm")
        await cog_function(cls, ctx, *args, **kwargs)

    return wrapper


def connect_db(function):
    """
    Decorator that creates a database object and inserts as its
    the first argument in the calling function.
    Useful to prevent global objects
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = None
        with dataset.connect(config.CONFIG.database_connection) as db:
            result = function(db, *args, **kwargs)
        return result

    return wrapper

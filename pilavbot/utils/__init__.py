from discord import Embed, Color

from utils.ext import *


async def pretty_print(ctx, fields, caption="", title="", color=Color(0xFFFFFF)):
    """
    A method for printing to the Discord channel with a custom embed.

    Parameters
    __________

      ctx (discord.Context) – The invocation context where the call was made
      fields (list or string) - Either a comma separated list of fields or a single string
                                Each field is organized by [Title, Value, Inline] as specified in Discord documentation
      caption (string) - A message to append to the bottom of the embed, useful for printing mentions and such
      title (string) - Title listed at the top of the embed
      color (string) - A Hexadecimal code representing the color strip on the left side of the Embed

    """

    if not ctx:
        return

    embed = Embed(title=title, color=color)

    if type(fields) == list:
        for field in fields:
            if len(field) < 3:
                field.append(True)

            name, value, inline = field
            embed.add_field(name=name, value=value, inline=inline)

    elif type(fields) == str:
        embed.add_field(name="-------------", value=fields)

    if caption:
        message = await ctx.send(content=caption, embed=embed)
    else:
        message =await ctx.send(embed=embed)

    return message
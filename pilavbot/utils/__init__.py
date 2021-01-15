from discord import Embed, Color

from utils.ext import *


async def pretty_print(ctx, fields, caption="", thumbnail="", title="", footer={}, timestamp=False, color=Color(0xFFFFFF)):
    """A method for printing to the Discord channel with a custom embed.

    Args:
        ctx (discord.Context): The invocation context where the call was made.
        fields (list or string): Either a comma separated list of fields(as dicts) or a single string.
            Each field is organized by [title, value, inline] as specified in Discord documentation.
        caption (string): A message to append to the top of the embed, useful for printing mentions and such.
        thumbnail (string): URL of the thumbnail.
        title (string): Title listed at the top of the embed.
        footer (dict): Footer dict with either of [text, icon_url] as key together with it's value.
        timestamp (bool): A bool to decide should the timestamp be added to the end of the Embed.
        color (string): A Hexadecimal code representing the color strip on the left side of the Embed.

    Returns:
        discord.message.Message: Message object itself.
    """

    if not ctx:
        return

    if timestamp:
        embed = Embed(
            title=title,
            color=color,
            timestamp=ctx.message.created_at,
        )
    else:
        embed = Embed(
            title=title,
            color=color,
        )

    if type(fields) == list:
        for field in fields:
            if len(field) < 3:
                field["inline"] = True

            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field["inline"]
            )
    elif type(fields) == str:
        embed.add_field(name="-------------", value=fields)

    if "text" in footer and "icon_url" in footer:
        embed.set_footer(text=footer["text"], icon_url=footer["icon_url"])
    elif "text" in footer:
        embed.set_footer(text=footer["text"]),
    elif "icon_url" in footer:
        embed.set_footer(icon_url=footer["icon_url"]),

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if caption:
        message = await ctx.send(content=caption, embed=embed)
    else:
        message = await ctx.send(embed=embed)

    return message

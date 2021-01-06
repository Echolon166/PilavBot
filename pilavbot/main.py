import threading

import discord
from discord.ext import commands, tasks

import config
import data
from constants import *

from cogs import *


if __name__ == "__main__":
    config.parse_args()
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    default_prefix = config.CONFIG.command_prefix

    def prefix(bot, ctx):
        try:
            guildId = ctx.guild.id
            return data.get_prefix(guildId) or default_prefix
        except:
            return default_prefix

    bot = commands.Bot(command_prefix=prefix, intents=intents)
    bot.add_cog(channel_cog.ChannelCommands(bot))
    bot.add_cog(options_cog.OptionsCommands(bot))
    
    for command in bot.commands:
        data.add_command(command.name, command.help)

    bot.run(config.CONFIG.secret_token)

import dataset
import datetime

import config
from constants import *

from utils.ext import connect_db

"""Functions for managing a dataset SQL database
    # Schemas
    
    #################### channel_prefixes ######################
    guildId
    prefix
    
    #################### commands ####################
    name
    description

    #################### config ####################
    configName
    joinEmoji
    startEmoji
"""


@connect_db
def add_prefix_mapping(db, guild_id, prefix):
    table = db[CHANNEL_PREFIXES_TABLE]
    table.upsert({GUILD_ID_KEY: guild_id, PREFIX_KEY: prefix}, [GUILD_ID_KEY])


@connect_db
def get_prefix(db, guild_id):

    table = db[CHANNEL_PREFIXES_TABLE]
    row = table.find_one(guildId=guild_id)
    if row is not None:
        return row[PREFIX_KEY]
    return None


@connect_db
def set_join_emoji(db, guild_id, join_emoji_str):
    table = db[CONFIG_TABLE]
    table.upsert(
        {
            GUILD_ID_KEY: guild_id,
            JOIN_EMOJI_KEY: join_emoji_str,
            CONFIG_NAME_KEY: JOIN_EMOJI_KEY,
        },
        [GUILD_ID_KEY, CONFIG_NAME_KEY],
    )


@connect_db
def get_join_emoji(db, guild_id):
    table = db[CONFIG_TABLE]
    row = table.find_one(guildId=guild_id, configName=JOIN_EMOJI_KEY)
    if row is not None:
        return row[JOIN_EMOJI_KEY]
    return None


@connect_db
def set_start_emoji(db, guild_id, message):
    table = db[CONFIG_TABLE]
    table.upsert(
        {
            GUILD_ID_KEY: guild_id,
            START_EMOJI_KEY: message,
            CONFIG_NAME_KEY: START_EMOJI_KEY,
        },
        [GUILD_ID_KEY, CONFIG_NAME_KEY],
    )


@connect_db
def get_start_emoji(db, guild_id):
    table = db[CONFIG_TABLE]
    row = table.find_one(guildId=guild_id, configName=START_EMOJI_KEY)
    if row is not None:
        return row[START_EMOJI_KEY]
    return None


@connect_db
def add_command(db, name, description):
    table = db[COMMANDS_TABLE]
    table.upsert(
        {
            NAME_KEY: name,
            DESCRIPTION_KEY: description,
        },
        [NAME_KEY],
    )


@connect_db
def get_all_commands(db):
    table = db[COMMANDS_TABLE]
    return table.all()

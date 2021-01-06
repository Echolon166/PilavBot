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
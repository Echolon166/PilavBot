from discord import Color

"""
    Constants useful for data module
"""

CHANNEL_PREFIXES_TABLE = "channel_prefixes"
COMMANDS_TABLE = "commands"
CONFIG_TABLE = "config"

GUILD_ID_KEY = "guildId"
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
PREFIX_KEY = "prefix"

CONFIG_NAME_KEY = "configName"
JOIN_EMOJI_KEY = "joinEmoji"
START_EMOJI_KEY = "startEmoji"


"""
    URL constants
"""

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
EXCHANGE_RATES_API_URL = "https://api.exchangeratesapi.io"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

WEATHER_ICON_URL = "http://openweathermap.org/img/w/"


"""
    Path constants
"""

ROOT_EMOJI_PATH = "assets/emojis/root"


"""
    Miscellaneous constants
"""

ERROR_COLOR = Color(0xFF0000)
SUCCESS_COLOR = Color(0x0000FF)
WHITE_COLOR = Color(0xFFFFFE)

DEFAULT_JOIN_EMOJI_STR = "👍"
DEFAULT_START_EMOJI_STR = "🚀"

WAIT_TIME = 0.8

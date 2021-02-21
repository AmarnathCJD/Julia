import logging
import os
import sys
import time
from logging import basicConfig
from logging import DEBUG
from logging import getLogger
from logging import INFO

from telethon import TelegramClient
from telethon.sessions import StringSession

StartTime = time.time()
CMD_LIST = {}
CMD_HELP = {}
LOAD_PLUG = {}
BOT_VERSION = "1.1.1"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", True))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    OWNER_ID = 1221693726
    GBAN_LOGS = os.environ.get("GBAN_LOGS", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
    DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    DB_URI = os.environ.get("DATABASE_URL")
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)
    tbot = TelegramClient(None, API_KEY, API_HASH)
    SUDO_USERS = list(SUDO_USERS)
    DEV_USERS = list(DEV_USERS)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    WALL_API = os.environ.get("WALL_API", None)
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    TEMPORARY_DATA = os.environ.get("TEMPORARY_DATA", None)
    UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO_URL", None)
    CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")
    BOT_ID = int(os.environ.get("BOT_ID", None))
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
        )
    LOGS = getLogger(__name__)

    if STRING_SESSION:
        ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        sys.exit(1)

    try:
        ubot.start()
    except BaseException:
        print("Sed Bra")
        sys.exit(1)

else:
    # Put your ppe vars here if you are using local hosting
    PLACEHOLDER = None
    TOKEN = "1484701846:AAEi08RPmT6fB4WTOAe6d87LBhnct1ScXMQ"
    OWNER_ID = 1221693726
    OWNER_USERNAME = "RoseLoverX"
    API_KEY = 1822414
    API_HASH = "46f1888d3f68396bad08c92ac4d7f00a"
    DB_URI = "postgres://okebzhizjpyfrf:792896d97d959a7fd4b1cb91c66bb621ec075aa83d8278728a33b77f8c3672a7@ec2-52-50-171-4.eu-west-1.compute.amazonaws.com:5432/d23aaaj6ddar4f"
    SUDO_USERS = None
    DEV_USERS = None
    UPSTREAM_REPO_URL = "https://github.com/amarnathcdj/julia"
    MONGO_DB_URI = "mongodb+srv://newgay:nub123@cluster0.hlrtz.mongodb.net/anie?retryWrites=true&w=majority"
    REM_BG_API_KEY = None
    TIME_API_KEY = None
    IBM_WATSON_CRED_URL = None
    TEMPORARY_DATA = None
    CONSOLE_LOGGER_VERBOSE = False
    BOT_ID = 1484701846
    CHROME_DRIVER = None
    GOOGLE_CHROME_BIN = None
    tbot = TelegramClient(None, API_KEY, API_HASH)
    LYDIA_API_KEY = None
    WOLFRAM_ID = None
    TEMP_DOWNLOAD_DIRECTORY = "./"
    YOUTUBE_API_KEY = None
    
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
        )
    LOGS = getLogger(__name__)

    if STRING_SESSION:
        ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        sys.exit(1)

    try:
        ubot.start()
    except BaseException:
        print("Sed Bra")
        sys.exit(1)

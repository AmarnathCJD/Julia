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

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", True))
if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    try:
        SPAMMERS = {int(x) for x in os.environ.get("SPAMMERS", "").split()}
    except ValueError:
        raise Exception(
            "Your spammers users list does not contain valid integers.")
    MESSAGE_DUMP = os.environ.get("MESSAGE_DUMP", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    try:
        SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your sudo users list does not contain valid integers.")
    try:
        SUPPORT_USERS = {int(x)
                         for x in os.environ.get("SUPPORT_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")
    try:
        WHITELIST_USERS = {
            int(x) for x in os.environ.get("WHITELIST_USERS", "").split()
        }
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    PORT = int(os.environ.get("PORT", 5432))
    CERT_PATH = os.environ.get("CERT_PATH")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    DB_URI = os.environ.get("DATABASE_URL")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_ANTISPAM = bool(os.environ.get("STRICT_ANTISPAM", True))
    DEEPFRY_TOKEN = os.environ.get("DEEPFRY_TOKEN", "")
    BOTLOG_CHATID = int(os.environ.get("MESSAGE_DUMP"))
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)
    WORKERS = int(os.environ.get("WORKERS", 8))
    WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)
    BAN_STICKER = os.environ.get(
        "BAN_STICKER",
        "CAACAgUAAxkBAALtC17p4EIAATVENsrWdMiTEinfiUXp3wACDwADTB0uPDaYvTB8iR7eGgQ",
    )
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    GBAN_LOGS = os.environ.get("MESSAGE_DUMP")
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)
    tbot = TelegramClient("alexa", API_KEY, API_HASH)

    SUDO_USERS = list(SUDO_USERS)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    WHITELIST_USERS = list(WHITELIST_USERS)
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    SUPPORT_USERS = list(SUPPORT_USERS)
    WALL_API = os.environ.get("WALL_API", None)
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)

    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    UPSTREAM_REPO_URL = os.environ.get(
        "UPSTREAM_REPO_URL", "https://github.com/MainTeraHer0/MissLillyRobot.git"
    )
    TEMPORARY_DATA = os.environ.get("TEMPORARY_DATA", None)

    CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")

    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
        )

    LOGS = getLogger(__name__)
    BOTLOG = os.environ.get("BOTLOG") == "True"

    if STRING_SESSION:
        ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        sys.exit(1)

    async def check_botlog_chatid():
        if not BOTLOG:
            return
        entity = await ubot.get_entity(BOTLOG_CHATID)
        if entity.default_banned_rights.send_messages:
            LOGS.error(
                "Your account doesn't have rights to send messages to BOTLOG_CHATID "
                "group. Check if you typed the Chat ID correctly. Halting!"
            )
            sys.exit(1)

    with ubot:
        try:
            ubot.loop.run_until_complete(check_botlog_chatid())
        except BaseException:
            LOGS.error(
                "BOTLOG_CHATID environment variable isn't a " "valid entity. Halting!"
            )
            sys.exit(1)

    try:
        ubot.start()
    except BaseException:
        print("Network Error !")
        sys.exit(1)

else:
    sys.exit(1)

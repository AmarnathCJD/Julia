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
    TOKEN = "1484701846:AAEi08RPmT6fB4WTOAe6d87LBhnct1ScXMQ"
    OWNER_ID = 1221693726
    OWNER_USERNAME = "RoseLoverX"
    API_KEY = 1822414
    API_HASH = "46f1888d3f68396bad08c92ac4d7f00a"
    DB_URI = "postgres://okebzhizjpyfrf:792896d97d959a7fd4b1cb91c66bb621ec075aa83d8278728a33b77f8c3672a7@ec2-52-50-171-4.eu-west-1.compute.amazonaws.com:5432/d23aaaj6ddar4f"
    su = 1383009042
    de = 1383009042
    SUDO_USERS = {int(x) for x in su.split()}
    DEV_USERS = {int(x) for x in de.split()}
    SUDO_USERS = list(SUDO_USERS)
    DEV_USERS = list(DEV_USERS)
    UPSTREAM_REPO_URL = "https://github.com/amarnathcdj/julia"
    MONGO_DB_URI = "mongodb+srv://newgay:nub123@cluster0.hlrtz.mongodb.net/anie?retryWrites=true&w=majority"
    REM_BG_API_KEY = None
    TIME_API_KEY = None
    IBM_WATSON_CRED_URL = None
    IBM_WATSON_CRED_PASSWORD = None
    HEROKU_APP_NAME = None
    TEMPORARY_DATA = None
    CONSOLE_LOGGER_VERBOSE = False
    BOT_ID = 1484701846
    CHROME_DRIVER = "/app/.chromedriver/bin/chromedriver"
    GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
    tbot = TelegramClient(None, API_KEY, API_HASH)
    LYDIA_API_KEY = None
    WOLFRAM_ID = "V4GHVG-AKHHG599KP"
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WALL_API = "e87add43be4c43a58c00ec5957ab250b"
    YOUTUBE_API_KEY = None
    VIRUS_API_KEY = None
    CASH_API_KEY = None
    OPENWEATHERMAP_ID = "dbab2b41c8871bb3ef0627d9ae4e4693"
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
        )
    LOGS = getLogger(__name__)
    STRING_SESSION = "1BVtsOIgBuxbp6HU1bRBeYEdSmNVKcuTjR8C5chKx2BqzyaIRTImT0Qj6YM-p-st0m_wTVORWMvRm1mT8CUcqRLhD52wfGhW203eoqsMrnDPMunoY7dkMjfFa80u-SFw8bMV8BA-rYHOyv1NhrPJijqkXGIqX3NSUUtYIE3lbM52r3Cavc17XR-k6OkTayCx8N2WaWjS_egO8XKJOr-jVkf_piwabAf2zLNXLea3IPZ5HF7IWy-YtJ1tIjdnh98biiMldh7wLTfwFyI-Ui0Rqfqz6nrFJazftue5QY-yHsNj9L9T2UhqsEHKlaV2Ox-NiLDvBmnBRUrnEKi3L_0EXfehIQypxvuw="
    if STRING_SESSION:
        ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        sys.exit(1)

    try:
        ubot.start()
    except BaseException:
        print("Sed Bra")
        sys.exit(1)

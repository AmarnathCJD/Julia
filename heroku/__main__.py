from heroku import tbot, ubot
from sys import argv, exit

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Error !")
    exit(1)

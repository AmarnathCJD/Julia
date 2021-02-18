import sys, subprocess, datetime
from julia import tbot
from julia.events import register
import secureme
@register(pattern="^/decrypt (.*)")
async def hmm(event):
   cmd = event.pattern_match.group(1)
   Text = cmd
   await encrypt(event, tbot)
   await event.reply("hmm")
   await event.reply(f"{encrypted}")
  




def encrypt(Text, Method="Length", Password="22"):
    args = ["HWID", "Length", "Password", "Date", "Month", "Year", "Hour"]
    if Method == "HWID":
        key = HWID()
    if Method == "Length":
        key = len(Text)
    if Method == "Password":
        key = Password
    if Method == "Date":
        key = datetime.datetime.now().day
    if Method == "Month":
        key = datetime.datetime.now().month
    if Method == "Year":
        key = datetime.datetime.now().year
    if Method == "Hour":
        key = datetime.datetime.now().hour
    if Method not in args:
        print(f"You have to pass one from {args} to encrypt or leave it blank.")
        sys.exit()
    encrypted = ''
    for i in Text :
        encrypted += top._alphabet[int((top._alphabet.find(i) + key) % len(top._alphabet))]
    return encrypted
def decrypt(Text, Method="Length", Password="22"):
    args = ["HWID", "Length", "Password", "Date", "Month", "Year", "Hour"]
    if Method == "HWID":
        key = HWID()
    if Method == "Length":
        key = len(Text)
    if Method == "Password":
        key = Password
    if Method == "Date":
        key = datetime.datetime.now().day
    if Method == "Month":
        key = datetime.datetime.now().month
    if Method == "Year":
        key = datetime.datetime.now().year
    if Method == "Hour":
        key = datetime.datetime.now().hour
    if Method not in args:
        print(f"You have to pass one from {args} to encrypt or leave it blank.")
        sys.exit()
    encrypted = ''
    for i in Text :
        encrypted += top._alphabet[int((top._alphabet.find(i) + key) % len(top._alphabet))]
    return encrypted

from julia import tbot
from telethon import *
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
import dateparser 

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
alarms = db.alarm

def get_reason(id):
    return alarms.find_one({"chat": id})

@register(pattern="^/setalarm (.*)")
async def _(event):
 try:
    if event.fwd_from:
        return    
    quew = event.pattern_match.group(1)
    if "|" in quew:
        iid, zonee, reasonn = quew.split("|")
    time = iid.strip()
    reason = reasonn.strip()
    zone = zonee.strip()
    if len(time) != 22:
      await event.reply("Please enter valid date and time.")
      return
    ttime = dateparser.parse(f'{time}', settings={'TIMEZONE': f'{zone}'}) 
    time = ttime # exchange
    present = dateparser.parse(f'now', settings={'TIMEZONE': f'{zone}'}) 
    #print(ttime)
    #print(present)
    if not time > present:
      await event.reply("Please enter valid date and time.")
      return
    if not reason:
        reason = "No reason given"
    chats = alarms.find({})
    for c in chats:
        if event.chat_id == c["chat"] and time == c["time"]:
            to_check = get_reason(id=event.chat_id)
            alarms.update_one({"_id": to_check["_id"], "chat": to_check["chat"], "user": to_check["user"], "time": to_check["time"], "zone": to_check["zone"], "reason": to_check["reason"]}, {
                               "$set": {"reason": reason, "zone": zone}})
            await event.reply("This alarm is already set.\nI am updating the reason(and zone) of the alarm with the new reason(and zone).")
            return
    alarms.insert_one({"chat": event.chat_id, "user": f"[user](tg://user?id={event.sender_id})", "time": time, "zone": zone, "reason": reason})
    await event.reply("Alarm set successfully !")
 except Exception as e:
    print (e)

global chat, user, time, zone, reason, present, ttime
@tbot.on(events.NewMessage(pattern=None))
@tbot.on(events.ChatAction())
async def tikclock(event):
    chats = alarms.find({})
    for c in chats:
     #print(c)
     chat = c["chat"]
     user = c["user"]
     time = c["time"]
     zone = c["zone"]
     reason = c["reason"]
     present = dateparser.parse(f'now', settings={'TIMEZONE': f'{zone}'}) 
     ttime = dateparser.parse(f'{time}', settings={'TIMEZONE': f'{zone}'}) 
     #print(ttime)
     #print(present)
     #print (zone)
     if not present >= ttime:
       return
     #print("loop passing")
     await tbot.send_message(chat, f"**DING DONG**\n\n__This is an alarm set by__ {user} __for reason -__ `{reason}`")
     alarms.delete_one({"chat": chat, "user": user, "time": time, "zone": zone, "reason": reason})
     

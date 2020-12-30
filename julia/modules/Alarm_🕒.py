from julia import tbot
from telethon import *
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
import dateparser, datetime

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
alarms = db.alarm

def get_reason(id):
    return alarms.find_one({"chat": id})

@register(pattern="^/setalarm (.*)")
async def _(event):
    if event.fwd_from:
        return    
    quew = event.pattern_match.group(1)
    
    if "|" in quew:
            iid, reasonn = quew.split("|")
    time = iid.strip()
    reason = reasonn.strip()
    ttime = dateparser.parse(time)  
    time = ttime # exchange
    if len(time) != 19:
      await event.reply("Please enter valid date and time")
      return
    
    if not reason:
        reason = "No reason given"
    chats = alarms.find({})

    for c in chats:
        if event.chat_id == c["chat"] and time == c["time"]:
            to_check = get_reason(id=event.chat_id)
            alarms.update_one({"_id": to_check["_id"], "chat": to_check["chat"], "user": to_check["user"], "time": to_check["time"], "reason": to_check["reason"]}, {
                               "$set": {"reason": reason}})
            await event.reply("This alarm is already set.\nI am updating the reason of the alarm with the new reason.")
            return
    alarms.insert_one({"chat": event.chat_id, "user": event.sender_id, "time": time, "reason": reason})
    await event.reply("Alarm set successfully !")



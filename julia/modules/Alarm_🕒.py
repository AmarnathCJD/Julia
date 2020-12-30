from julia import tbot
from telethon import *
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
import dateparser, datetime, pytz 

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
alarms = db.alarm

def get_reason(id):
    return alarms.find_one({"chat": id})

def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)
    dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt

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
    ltime = f"'{time}'"+", settings={'TIMEZONE': "+f"'{zone}'"+"}"
    ttime = dateparser.parse(ltime) 
    time = ttime # exchange
    print (ltime)
    print(ttime)
    resent = datetime.datetime.now()
    present = resent.strftime("%Y-%m-%d %H:%M:%S")
    gtime = convert_datetime_timezone(str(present), "America/New_York", zone)
    print(gtime)
    if gtime <= present:
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

@tbot.on(events.NewMessage(pattern=None))
@tbot.on(events.ChatAction())
async def tikclock(event):
    chats = alarms.find({})
    for c in chats:
      try:
        if event.chat_id == c["chat"]:
                to_check = get_reason(id=event.chat_id)
                reason = to_check["reason"]
                user = to_check["user"]
                time = to_check["time"]
                zone = to_check["zone"]
                present = datetime.datetime.now(pytz.timezone(zone))
                if time >= present:                   
                   await event.reply(f"**DING DONG**\n\n__This is an alarm set by__ {user} __for reason -__ `{reason}`")
                   alarms.delete_one({"chat": event.chat_id})
                   return
      except Exception as e:
         print(e)

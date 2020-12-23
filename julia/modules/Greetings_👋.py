import os
from telethon import events
from telethon.utils import pack_bot_file_id
from julia.events import register
from julia import tbot, CMD_HELP
from julia.modules.sql.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from julia.modules.sql.welcome_sql import (
    add_goodbye_setting,
    get_current_goodbye_settings,
    rm_goodbye_setting,
    update_previous_goodbye,
)
import julia.modules.sql.rules_sql as sql
from telethon import *
from telethon.tl import *
from julia import *
import random
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.functions.channels import EditBannedRequest
from pymongo import MongoClient
from telethon.tl.types import ChatBannedRights

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
botcheck = db.checkbot

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

imgg = Image.new('RGB', (300, 200), color ="white") 
fntt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 50)
dd = ImageDraw.Draw(imgg)
dd.text((50,50), "Loading ...", font=fntt, fill="black")
imgg.save('loadcheckbot.png')

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.change_info)


@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await tbot.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = (
                f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            )
            userid = a_user.id
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            rules = sql.get_rules(event.chat_id)
            if rules:
             chats = botcheck.find({})
             for c in chats:
              if event.chat_id == c["id"]:
               current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid),
                file=cws.media_file_id,
                buttons=[[Button.inline('Rules ✝️', data=f'start-rules-{userid}')], [Button.inline('I am not a bot ✔️', data=f'check-bot-{userid}')]],
               )
               await tbot(EditBannedRequest(event.chat_id, userid, MUTE_RIGHTS))
               update_previous_welcome(event.chat_id, current_message.id)           
              else:
               current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid),
                file=cws.media_file_id,
                buttons=[[Button.inline('Rules ✝️', data=f'start-rules-{userid}')]],
               )
               update_previous_welcome(event.chat_id, current_message.id)
            else:
             chats = botcheck.find({})
             for c in chats:
              if event.chat_id == c["id"]:
               current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid),
                file=cws.media_file_id,
                buttons=[[Button.inline('I am not a bot ✔️', data=f'check-bot-{userid}')]],
               )
               await tbot(EditBannedRequest(event.chat_id, userid, MUTE_RIGHTS))
               update_previous_welcome(event.chat_id, current_message.id)
              else:
               current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid),
                file=cws.media_file_id)
               update_previous_welcome(event.chat_id, current_message.id)

# -- @MissJulia_Robot (sassiet captcha ever) --#

@tbot.on(events.CallbackQuery(pattern=r"start-rules-(\d+)"))
async def rules_st(event):
    rules = sql.get_rules(event.chat_id)
    # print(rules)
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You haven't send that command !")
       return
    text = f"The rules for **{event.chat.title}** are:\n\n{rules}"
    try:
        await tbot.send_message(
            user_id,
            text,
            parse_mode="markdown",
            link_preview=False)
    except Exception:
        await event.answer("I can't send you the rules as you haven't started me in PM, first start me !", alert=True)

# -- @MissJulia_Robot -- #

@tbot.on(events.CallbackQuery(pattern=r"check-bot-(\d+)"))
async def cbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    chat_id = event.chat_id
    chat_title = event.chat.title
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    num = random.randint(1,9)
    img = Image.new('RGB', (300, 200), color ="white") 
    fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
    d = ImageDraw.Draw(img)
    d.text((110,50), str(num), font=fnt, fill="black")
    img.save('checkbot.png')
    try:      
      await tbot.send_message(user_id, f"Hi, please solve the below captcha to start speaking in **{chat_title}**")
      miid = await tbot.send_message(
            user_id,
            "Loading ...",
            file="loadcheckbot.png",
            parse_mode="markdown")
      tid = miid
      button=[[Button.inline('1', data=f'1-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('2', data=f'2-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('3', data=f'3-{user_id}-{num}-{chat_id}-{tid}'')], [Button.inline('4', data=f'4-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('5', data=f'5-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('6', data=f'6-{user_id}-{num}-{chat_id}-{tid}'')], [Button.inline('7', data=f'7-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('8', data=f'8-{user_id}-{num}-{chat_id}-{tid}''), Button.inline('9', data=f'9-{user_id}-{num}-{chat_id}-{tid}'')]]   
      await tbot.edit_message(tid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
    except Exception as e:
      print(e)
      await event.answer("I can't send you the captcha as you haven't started me in PM, first start me !", alert=True)

@tbot.on(events.CallbackQuery(pattern=r"1-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 1
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      

@tbot.on(events.CallbackQuery(pattern=r"2-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 2
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
          
@tbot.on(events.CallbackQuery(pattern=r"3-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 3
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@tbot.on(events.CallbackQuery(pattern=r"4-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 4
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@tbot.on(events.CallbackQuery(pattern=r"5-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 5
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
        
@tbot.on(events.CallbackQuery(pattern=r"6-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 6
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@tbot.on(events.CallbackQuery(pattern=r"7-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 7
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@tbot.on(events.CallbackQuery(pattern=r"8-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 8
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@tbot.on(events.CallbackQuery(pattern=r"9-(\d+)-(\d+)-(\d+)-(\d+)"))
async def checkbot(event):
    if event.sender.bot:
       return        
    user_id = int(event.pattern_match.group(1))        
    if not event.sender_id == user_id:
       await event.answer("You aren't the person whom should be verified.")
       return
    cnum = 9
    onum = int(event.pattern_match.group(2))
    chat_id = int(event.pattern_match.group(3))
    msgid= int(event.pattern_match.group(4))
    if cnum == onum:
      try:
       await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
       await tbot.edit_message(msgid, "Yep you are verified as a human being, you are unmuted in that chat.")
      except Exception:
       await event.answer("Sorry I don't have permission to unmute you please contact some administrator.", alert=True)
    else:
       await event.answer("Sorry you have selected a wrong button.\nTry Again !", alert=True)
       num = random.randint(1,9)
       img = Image.new('RGB', (300, 200), color ="white") 
       fnt = ImageFont.truetype("./.apt/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100)
       d = ImageDraw.Draw(img)
       d.text((110,50), str(num), font=fnt, fill="black")
       img.save('checkbot.png')
       button=[[Button.inline('1', data=f'1-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('2', data=f'2-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('3', data=f'3-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('4', data=f'4-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('5', data=f'5-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('6', data=f'6-{user_id}-{onum}-{chat_id}-{msgid}')], [Button.inline('7', data=f'7-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('8', data=f'8-{user_id}-{onum}-{chat_id}-{msgid}'), Button.inline('9', data=f'9-{user_id}-{onum}-{chat_id}-{msgid}')]]    
       await tbot.edit_message(msgid, "See the above image and press the exact button corresponding to the number in the image", file="checkbot.png", buttons=button)
      
@register(pattern="^/setwelcome")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, True, 0, tbot_api_file_id)
        await event.reply("Welcome message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0, None)
        await event.reply("Welcome message saved. ")


@register(pattern="^/clearwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.reply(
        "Welcome message cleared. "
        + "The previous welcome message was `{}`".format(cws.custom_welcome_message)
    )


@register(pattern="^/checkwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, "custom_welcome_message"):
        await event.reply(
           "This chat's welcome message is\n\n`{}`".format(cws.custom_welcome_message)
        )
    else:
        await event.reply("No welcome message found for this chat")

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_left:
            if cws.should_clean_goodbye:
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_goodbye
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await tbot.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = (
                f"@{me.username}" if me.username else f"[Me](tg://user?id={me.id})"
            )
            userid = a_user.id
            current_saved_goodbye_message = cws.custom_goodbye_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)

            current_message = await event.reply(
                current_saved_goodbye_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                ),
                file=cws.media_file_id,
            )
            update_previous_goodbye(event.chat_id, current_message.id)

@register(pattern="^/setgoodbye")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_goodbye_setting(event.chat_id, msg.message, True, 0, tbot_api_file_id)
        await event.reply("Goodbye message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_goodbye_setting(event.chat_id, input_str[1], True, 0, None)
        await event.reply("Goodbye message saved. ")


@register(pattern="^/cleargoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_goodbye_settings(event.chat_id)
    rm_goodbye_setting(event.chat_id)
    await event.reply(
        "Goodbye message cleared. "
        + "The previous goodbye message was `{}`".format(cws.custom_goodbye_message)
    )


@register(pattern="^/checkgoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if hasattr(cws, "custom_goodbye_message"):
        await event.reply(
           "This chat's goodbye message is\n\n`{}`".format(cws.custom_goodbye_message)
        )
    else:
        await event.reply("No goodbye message found for this chat")

@register(pattern="^/welcomecaptcha(?: |$)(.*)")
async def welcome_verify(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = botcheck.find({})
    if not input:
        for c in chats:
            if event.chat_id == c["id"]:
                await event.reply(
                    "Please provide some input yes or no.\n\nCurrent setting is : **on**"
                )
                return
        await event.reply(
            "Please provide some input yes or no.\n\nCurrent setting is : **off**"
        )
        return
    if input in "on":
        if event.is_group:
            chats = botcheck.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Welcome Captcha is already enabled for this chat.")
                    return
            botcheck.insert_one({"id": event.chat_id})
            await event.reply("Welcome Captcha enabled for this chat.")
    if input in "off":
        if event.is_group:
            chats = botcheck.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    botcheck.delete_one({"id": event.chat_id})
                    await event.reply(
                        "Welcome Captcha disabled for this chat.")
                    return
        await event.reply(
                    "Welcome Captcha enabled for this chat.")       
    
    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return
      

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**Welcome**
 - /setwelcome <welcome message> or <reply to a text>: Saves the message as a welcome note in the chat.
 - /checkwelcome: Check whether you have a welcome note in the chat.
 - /clearwelcome: Deletes the welcome note for the current chat.
 - /welcomecaptcha <on/off>: Mutes a user on joining and unmutes as he/she solves a image captcha.

**Goodbye**
 - /setgoodbye <goodbye message> or <reply to a text>: Saves the message as a goodbye note in the chat.
 - /checkgoodbye: Check whether you have a goodbye note in the chat.
 - /cleargoodbye: Deletes the goodbye note for the current chat.

**Available variables for formatting greeting message:**
`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`

**Note**: __You can't set new welcome/goodbye message before deleting the previous one.__
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

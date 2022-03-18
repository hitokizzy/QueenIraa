import os
import re
import random
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from geezram.events import register
from geezram import telethn as tbot


PHOTO = [
 "https://telegra.ph/file/3b757c3986ec72f09096c.jpg"
]

@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**Hallo [{event.sender.first_name}](tg://user?id={event.sender.id}),\n\nsaya Queen Iraa​.**\n━━━━━━━━━━━━━━━━━━━\n\n"
  TEXT += f"» **ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ​ : [GEEZ/RAM](https://t.me/xnxx)** \n\n"
  TEXT += f"» **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{telever}` \n\n"
  TEXT += f"» **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tlhver}` \n\n"
  TEXT += f"» **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
  BUTTON = [[Button.url("RAM", "https://t.me/ramsupportt?start=help"), Button.url("GEEZ", "https://t.me/GeezSupport")]]
  ran = random.choice(PHOTO)
  await tbot.send_file(event.chat_id, ran, caption=TEXT,  buttons=BUTTON)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from geezram import pbot as client


@client.on_message(filters.command("dev"))
async def start(client, message):
    await message.reply(
            "halo, saya bot dari Geez dan Ram",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("GEEZ", url="https://t.me/GeezSupport")]
                [InlineKeyboardButton("RAM", url="https://t.me/ramsupportt")]
                ]
            )
        )

## Ramdi Module  😂
__mod_name__ = "Ramdi"

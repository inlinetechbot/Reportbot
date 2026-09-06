import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from info import Config, Txt


@Client.on_message(filters.private & filters.command('start'))
async def handle_start(bot:Client, message:Message):

    Btn = [
        [InlineKeyboardButton(text='❗Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='🌀Sᴇʀᴠᴇʀ Sᴛᴀᴛs', callback_data='server')],
        [InlineKeyboardButton(text='🌻Uᴘᴅᴀᴛᴇs', url='https://t.me/voxcry'), InlineKeyboardButton(text='🌨️Aʙᴏᴜᴛ', callback_data='about')],
        [InlineKeyboardButton(text='❄️Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/voxcry')]
        ]

    await message.reply_text(text=Txt.START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(Btn))


#Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.OWNER))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)

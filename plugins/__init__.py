import os
import sys
import asyncio
from config import Config
from translation import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
from main import LOGGER, prefixes, AUTH_USERS
  
from .test import CLIENT 

main_buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/venombotupdates'),
        InlineKeyboardButton('📢 Update Channel ', url='https://t.me/venombotsupport')
        ],[
        InlineKeyboardButton('❗️Help', callback_data='help') 
        ],[
        
]]

#===================Start Function===================#

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.START_TXT.format(
                message.from_user.first_name))

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.AUTH_USERS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying to restarting.....</i>"
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
            InlineKeyboardButton('💠 About 💠', callback_data='about'),
            InlineKeyboardButton('💠 Status 💠', callback_data='status'),
            ],[
            InlineKeyboardButton('💠 How To Use Me ? 💠', callback_data='how_to_use')
            ],[
            InlineKeyboardButton('💠 Settings 💠', callback_data='settings#main')
            ],[
            InlineKeyboardButton('• back', callback_data='back')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Translation.HELP_TXT,
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Translation.HOW_USE_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Translation.START_TXT.format(
                query.from_user.first_name))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Translation.ABOUT_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )


@Client.on_message(
    filters.chat(AUTH_USERS) & filters.private &
    filters.incoming & filters.command("cancel", prefixes=prefixes)
)
async def restart_handler(_, m):
    await m.reply_text("Forwarding stopped", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(
    filters.chat(AUTH_USERS) & filters.private &
    filters.incoming & filters.command("log", prefixes=prefixes)
)
async def log_msg(client, message):
    await client.send_document(message.chat.id, "log.txt") 

@Client.on_message(filters.command('settings'))
async def settings(client, message):
   await message.reply_text(
     "<b>change your settings as your wish</b>",
     reply_markup=main_buttons()
     )
    
@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  i, type = query.data.split("#")
  buttons = [[InlineKeyboardButton('back', callback_data="settings#main")]]
  
  if type=="main":
     await query.message.edit_text(
       "<b>change your settings as your wish</b>",
       reply_markup=main_buttons())
       
  elif type=="bots":
     buttons = [] 
     _bot = await db.get_bot(user_id)
     if _bot is not None:
        buttons.append([InlineKeyboardButton(_bot['name'],
                         callback_data=f"settings#editbot")])
     else:
        buttons.append([InlineKeyboardButton('✚ Add bot ✚', 
                         callback_data="settings#addbot")])
        buttons.append([InlineKeyboardButton('✚ Add User bot ✚', 
                         callback_data="settings#adduserbot")])
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
       "<b><u>My Bots</b></u>\n\n<b>You can manage your bots in here</b>",
       reply_markup=InlineKeyboardMarkup(buttons))
  
  elif type=="addbot":
     await query.message.delete()
     bot = await CLIENT.add_bot(bot, query)
     if bot != True: return
     await query.message.reply_text(
        "<b>bot token successfully added to db</b>",
        reply_markup=InlineKeyboardMarkup(buttons)) 

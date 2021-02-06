from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from pyrogram import filters
from wbb import app
from wbb.utils.botinfo import BOT_ID
from wbb import LYDIA_API

__MODULE__ = 'Lydia'
__HELP__ = "Lydia AI Chatbot"

CoffeeHouseAPI = API(str(LYDIA_API))
api_ = LydiaAI(CoffeeHouseAPI)
chats = []
ses = None

@app.on_message(filters.command('addchatbot'))
async def add_chat(_, message):
    global chats, api_, ses
    if message.chat.id not in chats:
        ses = api_.create_session()
        chats.append(message.chat.id)
        await message.reply_text('ChatBot enabled!')
    else:
        await message.reply_text('ChatBot Is Already Enabled')


@app.on_message(filters.command('rmchatbot'))
async def remove_chat(_, message):
    global chats
    if message.chats.id not in chats:
        await message.reply_text("ChatBot Is Already Off")
    else:
        chats.remove(message.chat.id)
        await message.reply_text('ChatBot Turned Off!')


@app.on_message(~filters.edited & ~filters.private)
async def chat_bot(_, message):
    global api_, chats, ses
    if message.chat.id not in chats:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user.id == BOT_ID:
        return
    if not message.text:
        return
    await app.send_chat_action(message.chat.id, "typing")
    query = message.text
    rep = api_.think_thought(text=query, session_id=ses.id)
    await message.reply_text(rep)

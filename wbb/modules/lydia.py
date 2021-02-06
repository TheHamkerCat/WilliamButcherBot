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
is_chat = False
ses = None

@app.on_message(filters.command('addchatbot'))
async def add_chat(_, message):
    global is_chat, api_, ses
    if not is_chat:
        ses = api_.create_session()
        is_chat = True
        await message.reply_text('ChatBot enabled!')
    else:
        await message.reply_text('ChatBot Is Already Enabled')


@app.on_message(filters.command('rmchatbot'))
async def remove_chat(_, message):
    global is_chat
    if not is_chat:
        await message.reply_text("ChatBot Is Already Off")
    else:
        await message.reply_text('ChatBot Turned Off!')


@app.on_message(~filters.edited & ~filters.private)
async def chat_bot(_, message):
    global api_, is_chat, ses
    if not is_chat:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user.id == BOT_ID:
        return
    query = message.text
    rep = api_.think_thought(text=query, session_id=ses.id)
    await message.reply_text(rep)

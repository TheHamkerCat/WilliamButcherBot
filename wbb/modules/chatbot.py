import aiohttp
from pyrogram import filters
from wbb import app
from wbb.utils.botinfo import BOT_ID


__MODULE__ = 'Chatbot'
__HELP__ = "Reply To Any Message Of Bot To See This In Action."


async def getresp(query):
    url = f"https://dsghrfgj.herokuapp.com/?query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res = await res.json()
            text = res['response']['bot']
            return text


@app.on_message(~filters.edited & filters.reply)
async def chat_bot(_, message):
    if not message.reply_to_message.from_user.id == BOT_ID:
        return
    if not message.text:
        query = "Hello"
    else:
        query = message.text
    await app.send_chat_action(message.chat.id, "typing")
    try:
        res = await getresp(query)
    except Exception as e:
        res = str(e)
    await message.reply_text(res)
    await app.send_chat_action(message.chat.id, "cancel")

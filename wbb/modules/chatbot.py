from pyrogram import filters
from wbb import app
from wbb.utils.botinfo import BOT_ID
import asyncio
import random
import aiohttp

__MODULE__ = 'Chatbot'
__HELP__ = "Reply To Any Message Of Bot To See This In Action."


@app.on_message(~filters.edited & ~filters.private & filters.text & filters.reply & ~filters.forwarded)
async def chat_bot(_, message):
    if not message.reply_to_message.from_user.id == BOT_ID:
        return
    await app.send_chat_action(message.chat.id, "typing")
    query = message.text
    url = f"https://dsghrfgj.herokuapp.com/?query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res = await res.json()
            res = res['response']['bot']
    await asyncio.sleep(random.randint(2,5))
    await message.reply_text(res)

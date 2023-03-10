# (c) @HYBRID_Bots

import random
import asyncio
from wbb import app # This is bot's client
from wbb import app2 # userbot client, import it if module is related to userbot
from wbb import SLAP_STICKERS # this is sticker id variable
from pyrogram import filters # pyrogram filters


# For /help menu
__MODULE__ = "Slap"
__HELP__ = "Reply with /slap to slap a user 😁"


@app.on_message(filters.command("slap"))
async def slap_user(_, message):
    # Check if the command was replied to a user
    if message.reply_to_message is None or not message.reply_to_message.from_user:
        reply_msg = await message.reply("Reply to a user that you wanna slap.")
        await message.delete()
        await asyncio.sleep(5)
        await reply_msg.delete()  
        return
    user_to_slap = message.reply_to_message.from_user
    slap_sticker = random.choice(SLAP_STICKERS)
    await message.reply_to_message.reply_sticker(sticker=slap_sticker)
    await message.delete()
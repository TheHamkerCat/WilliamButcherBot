"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from wbb import BOT_ID, SUDOERS, USERBOT_ID, app, app2
from wbb.core.decorators.errors import capture_err

__MODULE__ = "Pipes"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

Use this module to create a pipe that will forward messages of one chat/channel to another.


/activate_pipe [FROM_CHAT_ID] [TO_CHAT_ID] [BOT|USERBOT]

    Active a pipe.

    choose 'BOT' or 'USERBOT' according to your needs,
    this will decide which client will fetch the
    message from 'FROM_CHAT'.


/deactivate_pipe [FROM_CHAT_ID]
    Deactivete a pipe.


/show_pipes
    Show all the active pipes.

**NOTE:**
    These pipes are only temporary, and will be destroyed
    on restart.
"""
pipes_list_bot = {}
pipes_list_userbot = {}


@app.on_message(~filters.me, group=500)
@capture_err
async def pipes_worker_bot(_, message: Message):
    chat_id = message.chat.id
    if chat_id in pipes_list_bot:
        await message.forward(pipes_list_bot[chat_id])


@app2.on_message(~filters.me, group=500)
@capture_err
async def pipes_worker_userbot(_, message: Message):
    chat_id = message.chat.id

    if chat_id in pipes_list_bot:
        caption = f"\n\nForwarded from `{chat_id}`"
        to_chat_id = pipes_list_bot[chat_id]

        if not message.text:
            m, temp = await asyncio.gather(
                app.listen(USERBOT_ID), message.copy(BOT_ID)
            )
            caption = f"{temp.caption}{caption}" if temp.caption else caption

            await app.copy_message(
                to_chat_id,
                USERBOT_ID,
                m.message_id,
                caption=caption,
            )
            await asyncio.sleep(2)
            return await temp.delete()

        await app.send_message(to_chat_id, text=message.text + caption)


@app.on_message(filters.command("activate_pipe") & filters.user(SUDOERS))
@capture_err
async def activate_pipe_func(_, message: Message):
    global pipes_list_bot, pipes_list_userbot

    if len(message.command) != 4:
        return await message.reply(
            "**Usage:**\n/activate_pipe [FROM_CHAT_ID] [TO_CHAT_ID] [BOT|USERBOT]"
        )

    text = message.text.strip().split()

    from_chat = int(text[1])
    to_chat = int(text[2])
    fetcher = text[3].lower()

    if fetcher not in ["bot", "userbot"]:
        return await message.reply("Wrong fetcher, see help menu.")

    if from_chat in pipes_list_bot or from_chat in pipes_list_userbot:
        return await message.reply_text("This pipe is already active.")

    dict_ = pipes_list_bot
    if fetcher == "userbot":
        dict_ = pipes_list_userbot

    dict_[from_chat] = to_chat
    await message.reply_text("Activated pipe.")


@app.on_message(filters.command("deactivate_pipe") & filters.user(SUDOERS))
@capture_err
async def deactivate_pipe_func(_, message: Message):
    global pipes_list_bot, pipes_list_userbot

    if len(message.command) != 2:
        await message.reply_text("**Usage:**\n/deactivate_pipe [FROM_CHAT_ID]")
        return
    text = message.text.strip().split()
    from_chat = int(text[1])

    if from_chat not in pipes_list_bot and from_chat not in pipes_list_userbot:
        await message.reply_text("This pipe is already inactive.")

    dict_ = pipes_list_bot
    if from_chat in pipes_list_userbot:
        dict_ = pipes_list_userbot

    del dict_[from_chat]
    await message.reply_text("Deactivated pipe.")


@app.on_message(filters.command("pipes") & filters.user(SUDOERS))
@capture_err
async def show_pipes_func(_, message: Message):
    pipes_list_bot.update(pipes_list_userbot)
    if not pipes_list_bot:
        return await message.reply_text("No pipe is active.")

    text = ""
    for count, pipe in enumerate(pipes_list_bot.items(), 1):
        text += (
            f"**Pipe:** `{count}`\n**From:** `{pipe[0]}`\n"
            + f"**To:** `{pipe[1]}`\n\n"
        )
    await message.reply_text(text)

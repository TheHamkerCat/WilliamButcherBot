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
from wbb.utils.dbfunctions import (activate_pipe, deactivate_pipe,
                                   is_pipe_active, show_pipes)
from wbb.utils.filter_groups import pipes_group

__MODULE__ = "Pipes"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

Use this module to create a pipe that will forward messages of one chat/channel to another.


/activate_pipe [FROM_CHAT_ID] [TO_CHAT_ID] [BOT|USERBOT]

Active a pipe.

choose 'BOT' or 'USERBOT' according to your needs, this will decide
which client will fetch the message from 'FROM_CHAT'.


/deactivate_pipe [FROM_CHAT_ID] [TO_CHAT_ID]

Deactivete a pipe.


/show_pipes

Show all the active pipes.
"""
pipes_list_bot = []
pipes_list_userbot = []


async def load_pipes():
    print("[INFO]: LOADING PIPES")
    global pipes_list_bot, pipes_list_userbot
    pipes_list_bot = []
    pipes_list_userbot = []
    pipes = await show_pipes()
    for pipe in pipes:
        if pipe["fetcher"] == "bot":
            pipes_list_bot.append(pipe)
            continue
        pipes_list_userbot.append(pipe)
    print("[INFO]: LOADED PIPES")


loop = asyncio.get_running_loop()
loop.create_task(load_pipes())


@app.on_message(~filters.me, group=pipes_group)
@capture_err
async def pipes_worker_bot(_, message: Message):
    for pipe in pipes_list_bot:
        if pipe["from_chat_id"] == message.chat.id:
            await message.forward(pipe["to_chat_id"])


@app2.on_message(~filters.me, group=pipes_group)
@capture_err
async def pipes_worker_userbot(_, message: Message):
    for pipe in pipes_list_userbot:
        if pipe["from_chat_id"] == message.chat.id:
            if not message.text:
                m, temp = await asyncio.gather(
                    app.listen(USERBOT_ID), message.copy(BOT_ID)
                )
                caption = f"Forwarded from `{pipe['from_chat_id']}`"
                caption = (
                    f"{temp.caption}\n\n{caption}" if temp.caption else caption
                )
                await app.copy_message(
                    pipe["to_chat_id"],
                    USERBOT_ID,
                    m.message_id,
                    caption=caption,
                )
                await asyncio.sleep(10)
                await temp.delete()
                return
            caption = f"Forwarded from `{pipe['from_chat_id']}`"
            await app.send_message(
                pipe["to_chat_id"], text=message.text + "\n\n" + caption
            )


@app.on_message(filters.command("activate_pipe") & filters.user(SUDOERS))
@capture_err
async def activate_pipe_func(_, message: Message):
    if len(message.command) != 4:
        await message.reply_text(
            "**Usage:**\n/activate_pipe [FROM_CHAT_ID] [TO_CHAT_ID] [BOT|USERBOT]"
        )
        return
    text = message.text.strip().split()
    from_chat = int(text[1])
    to_chat = int(text[2])
    fetcher = text[3].lower()
    if fetcher != "bot" and fetcher != "userbot":
        await message.reply_text("Wrong fetcher, see help menu.")
        return
    if await is_pipe_active(from_chat, to_chat):
        await message.reply_text("This pipe is already active.")
        return
    await activate_pipe(from_chat, to_chat, fetcher)
    await load_pipes()
    await message.reply_text("Activated pipe.")


@app.on_message(filters.command("deactivate_pipe") & filters.user(SUDOERS))
@capture_err
async def deactivate_pipe_func(_, message: Message):
    if len(message.command) != 3:
        await message.reply_text(
            "**Usage:**\n/deactivate_pipe [FROM_CHAT_ID] [TO_CHAT_ID]"
        )
        return
    text = message.text.strip().split()
    from_chat = int(text[1])
    to_chat = int(text[2])
    if not await is_pipe_active(from_chat, to_chat):
        await message.reply_text("This pipe is already inactive.")
        return
    await deactivate_pipe(from_chat, to_chat)
    await load_pipes()
    await message.reply_text("Deactivated pipe.")


@app.on_message(filters.command("pipes") & filters.user(SUDOERS))
@capture_err
async def show_pipes_func(_, message: Message):
    pipes = pipes_list_bot + pipes_list_userbot
    if not pipes:
        await message.reply_text("No pipe is active.")
        return
    text = ""
    for count, pipe in enumerate(pipes, 1):
        text += (
            f"**Pipe:** `{count}`\n**From:** `{pipe['from_chat_id']}`\n"
            + f"**To:** `{pipe['to_chat_id']}`\n**Fetcher:** `{pipe['fetcher']}`\n\n"
        )
    await message.reply_text(text)

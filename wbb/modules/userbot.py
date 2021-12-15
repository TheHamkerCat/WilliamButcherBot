"""
    CREDITS:
        MOST OF THE CODE IN THIS FILE IS WRITTEN BY @Pokurt.
        SOURCE:
            https://github.com/pokurt/Nana-Remix/blob/master/nana/plugins/devs.py
"""

import os
import re
import subprocess
import sys
import traceback
from asyncio import sleep
from html import escape
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, ReplyKeyboardMarkup

from wbb import app2  # don't remove
from wbb import SUDOERS, USERBOT_PREFIX, app, arq, eor
from wbb.core.keyboard import ikb
from wbb.core.tasks import add_task, rm_task

# Eval and Sh module from nana-remix

m = None
p = print
r = None
arrow = lambda x: (x.text if isinstance(x, Message) else "") + "\n`→`"


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def iter_edit(message: Message, text: str):
    async for m in app2.iter_history(message.chat.id):

        # If no replies found, reply
        if m.message_id == message.message_id:
            return 0

        if not m.from_user or not m.text or not m.reply_to_message:
            continue

        if (
            (m.reply_to_message.message_id == message.message_id)
            and (m.from_user.id == message.from_user.id)
            and ("→" in m.text)
        ):
            try:
                return await m.edit(text)
            except MessageNotModified:
                return


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("eval", prefixes=USERBOT_PREFIX)
)
async def executor(client, message: Message):
    global m, p, r
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()

    if message.chat.type == "channel":
        return

    m = message
    p = print

    # To prevent keyboard input attacks
    if m.reply_to_message:
        r = m.reply_to_message
        if r.reply_markup and isinstance(r.reply_markup, ReplyKeyboardMarkup):
            return await eor(m, text="INSECURE!")
    status = None
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        task, task_id = await add_task(
            aexec,
            "Eval",
            cmd,
            client,
            m,
        )

        text = f"{arrow('')} Pending Task `{task_id}`"
        if not message.edit_date:
            status = await m.reply(text, quote=True)

        await task
    except Exception as e:
        e = traceback.format_exc()
        print(e)
        exc = e.splitlines()[-1]

    await rm_task()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"**→**\n`{escape(evaluation.strip())}`"

    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        await message.reply_document(
            document=filename,
            caption="`→`\n  **Attached Document**",
            quote=False,
        )
        os.remove(filename)
        if status:
            await status.delete()
        return

    # Edit the output if input is edited
    if message.edit_date:
        status_ = await iter_edit(message, final_output)
        if status_ == 0:
            return await message.reply(final_output, quote=True)
        return
    if not status.from_user:
        status = await app2.get_messages(status.chat.id, status.message_id)
    await eor(status, text=final_output, quote=True)


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & ~filters.edited
    & filters.command("sh", prefixes=USERBOT_PREFIX),
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="**Usage:**\n/sh git pull")

    if message.reply_to_message:
        r = message.reply_to_message
        if r.reply_markup and isinstance(
            r.reply_markup,
            ReplyKeyboardMarkup,
        ):
            return await eor(message, text="INSECURE!")

    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await eor(
                    message,
                    text=f"**INPUT:**\n```{escape(text)}```\n\n**ERROR:**\n```{escape(err)}```",
                )
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a, _ in enumerate(shell):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            errors = traceback.format_exc()
            return await eor(
                message,
                text=f"**INPUT:**\n```{escape(text)}```\n\n**ERROR:**\n```{''.join(errors)}```",
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app2.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption=escape(text),
            )
            return os.remove("output.txt")
        await eor(
            message,
            text=f"**INPUT:**\n```{escape(text)}```\n\n**OUTPUT:**\n```{escape(output)}```",
        )
    else:
        await eor(
            message,
            text=f"**INPUT:**\n```{escape(text)}```\n\n**OUTPUT: **\n`No output`",
        )

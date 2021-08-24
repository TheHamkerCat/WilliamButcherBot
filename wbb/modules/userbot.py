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
from asyncio import Lock, create_task
from html import escape
from inspect import getfullargspec
from io import StringIO

from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, ReplyKeyboardMarkup

from wbb import app  # don't remove
from wbb import SUDOERS, USERBOT_PREFIX, app2, arq

# Eval and Sh module from nana-remix

m = None
p = print
r = None
arq = arq
arrow = lambda x: x.text + "\n`→`"
TASKS_LOCK = Lock()
tasks = {}


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(
        **{k: v for k, v in kwargs.items() if k in spec}
    )


async def add_task(taskFunc, task_id, *args, **kwargs):
    global tasks
    task = create_task(taskFunc(*args, **kwargs))
    tasks[task_id] = task
    return task


async def rm_task(task_id=None):
    global tasks
    async with TASKS_LOCK:
        for key, value in list(tasks.items()):
            if value.done() or value.cancelled():
                del tasks[key]

        if task_id:
            if task_id in tasks:
                if not tasks[task_id].done():
                    tasks[task_id].cancel()
                del tasks[task_id]


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("cancelTask", prefixes=USERBOT_PREFIX)
)
async def task_cancel(_, message: Message):
    global tasks
    m = message
    r = m.reply_to_message

    if len(m.text.split()) == 2:
        mid = int(m.text.split(None, 1)[1])
    else:
        mid = r.message_id if r else None

    if not mid or not tasks:
        return await m.delete()

    if mid not in tasks:
        return await m.delete()

    await rm_task(mid)
    await eor(message, text=f"{arrow(m)} Task cancelled")


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("lsTasks", prefixes=USERBOT_PREFIX)
)
async def task_list(_, message: Message):
    await rm_task()
    if not tasks:
        return await eor(
            message,
            text=f"{arrow(message)} No tasks pending",
        )

    ls = "\n    ".join([str(i) for i in tasks.keys()])
    await eor(message, text=f"{arrow(message)}  {ls}")


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("eval", prefixes=USERBOT_PREFIX)
)
async def executor(client, message: Message):
    global m, p, r, tasks
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
        if r.reply_markup:
            if isinstance(r.reply_markup, ReplyKeyboardMarkup):
                return await eor(m, text="INSECURE!")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        task = await add_task(
            aexec,
            m.message_id,
            cmd,
            client,
            message,
        )
        await task
    except Exception as e:
        exc = str(e)

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
        # Save the last stdout in globals,
        # Can use the it in next calls
        globals()["lstdout"] = stdout
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
    else:
        mid = message.message_id

        # Edit the output if input is edited
        if message.edit_date:
            async for m in app2.iter_history(message.chat.id):

                # If no replies found, reply
                if m.message_id == mid:
                    break

                if (
                    not m.from_user
                    or not m.text
                    or not m.reply_to_message
                ):
                    continue

                if m.reply_to_message.message_id == mid:
                    if m.from_user.id == message.from_user.id:

                        if "→" in m.text:
                            try:
                                return await m.edit(final_output)
                            except MessageNotModified:
                                return
        await message.reply(final_output, quote=True)


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & ~filters.edited
    & filters.command("sh", prefixes=USERBOT_PREFIX),
)
async def shellrunner(client, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="**Usage:**\n/sh git pull")

    if message.reply_to_message:
        r = message.reply_to_message
        if r.reply_markup:
            if isinstance(r.reply_markup, ReplyKeyboardMarkup):
                return await eor(message, text="INSECURE!")

    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(
                """ (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x
            )
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
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
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

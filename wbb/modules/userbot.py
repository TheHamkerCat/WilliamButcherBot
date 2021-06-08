"""
    CREDITS:
        EVAL AND SH FUNCTION IN THIS MODULE IS WRITTEN BY @Pokurt.
        SOURCE:
            https://github.com/pokurt/Nana-Remix/blob/master/nana/plugins/devs.py
"""

import os
import re
import subprocess
import sys
import traceback
from html import escape
from inspect import getfullargspec
from io import StringIO

import aiofiles
from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_PREFIX, app, app2, arq
from wbb.core.decorators.misc import exec_time

__MODULE__ = "Userbot"
__HELP__ = """
.alive - Send Alive Message.
.l - Execute Python Code.
.sh - Execute Shell Code.
.approve | .disapprove - Approve Or Disapprove A User To PM You.
.block | .unblock - Block Or Unblock A User.
"""

# Eval and Sh module from nana-remix

m = None
p = print
r = None
exec_time = exec_time
arq = arq


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("l", prefixes=USERBOT_PREFIX)
)
async def executor(client, message: Message):
    global m, p, r
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    m = message
    p = print
    if message.reply_to_message:
        r = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
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
    final_output = f"**INPUT:**\n```{escape(cmd)}```\n\n**OUTPUT**:\n```{escape(evaluation.strip())}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**INPUT:**\n`{escape(cmd[0:980])}`\n\n**OUTPUT:**\n`Attached Document`",
            quote=False,
        )
        await message.delete()
        os.remove(filename)
    else:
        await edit_or_reply(message, text=final_output)


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command("sh", prefixes=USERBOT_PREFIX),
)
async def shellrunner(client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**Usage:**\n/sh git pull")
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
                await edit_or_reply(
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
            return await edit_or_reply(
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
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output`",
            )
            return os.remove("output.txt")
        await edit_or_reply(
            message,
            text=f"**INPUT:**\n```{escape(text)}```\n\n**OUTPUT:**\n```{escape(output)}```",
        )
    else:
        await edit_or_reply(
            message,
            text=f"**INPUT:**\n```{escape(text)}```\n\n**OUTPUT: **\n`No output`",
        )


""" C and CPP Eval """


async def sendFile(message: Message, text: str):
    file = "output.txt"
    async with aiofiles.open(file, mode="w+") as f:
        await f.write(text)
    await message.reply_document(file)
    os.remove(file)


@app2.on_message(
    filters.command(["c", "cpp"], prefixes=USERBOT_PREFIX)
    & filters.user(SUDOERS)
)
async def c_cpp_eval(_, message: Message):
    code = message.text.split(None, 1)[1]
    file = "exec.c"
    compiler = "g++"
    out = "exec"
    cmdCompile = [compiler, "-g", file, "-o", out]
    cmdRun = [f"./{out}"]
    async with aiofiles.open(file, mode="w+") as f:
        await f.write(code)
    pCompile = subprocess.run(cmdCompile, capture_output=True)
    os.remove(file)
    err = pCompile.stderr.decode()
    if err:
        text = f"**INPUT:**\n```{escape(code)}```\n\n**COMPILE-TIME ERROR:**```{escape(err)}```"
        if len(text) > 4090:
            return await sendFile(message, text)
        return await edit_or_reply(message, text=text)
    pRun = subprocess.run(cmdRun, capture_output=True)
    os.remove(out)
    err = pRun.stderr.decode()
    out = pRun.stdout.decode()
    err = f"**RUNTIME ERROR:**\n```{escape(err)}```" if err else None
    out = f"**OUTPUT:**\n```{escape(out)}```" if out else None
    text = f"**INPUT:**\n```{escape(code)}```\n\n{err if err else out}"
    if len(text) > 4090:
        return await sendFile(message, text)
    await edit_or_reply(message, text=text)

import sys
import traceback
from io import StringIO
import os
from inspect import getfullargspec
from wbb import app, OWNER_ID
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "Eval"
__HELP__ = "/eval - You know what this does lol"


# Eval module from nana-remix

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


@app.on_message(filters.user(OWNER_ID) & ~filters.forwarded & ~filters.via_bot & filters.command("eval"))
async def executor(client, message):
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
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
    final_output = (f"**OUTPUT**:\n```{evaluation.strip()}```")
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await message.delete()
    else:
        await edit_or_reply(message, text=final_output)

from os import remove
from os.path import isfile
from time import ctime, time

from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_PREFIX, app2
from wbb.core.sections import section
from wbb.modules.userbot import add_task, eor, rm_task
from wbb.utils.downloader import download


@app2.on_message(
    filters.user(SUDOERS)
    & filters.command("download", prefixes=USERBOT_PREFIX)
)
async def download_func(_, message: Message):
    reply = message.reply_to_message
    start = time()
    task_id = int(start)

    body = {
        "Started": ctime(start),
        "Task ID": task_id,
    }
    m = await eor(
        message,
        text=section("Downloading", body),
    )

    if reply:
        task = await add_task(
            reply.download,
            task_id=task_id,
            task_name="Downloader",
        )
        await task
        await rm_task(task_id)

        elapsed = int(time() - start)
        body["Took"] = f"{elapsed}s"

        return await eor(m, text=section("Downloaded", body))

    text = message.text
    if len(text.split()) < 2:
        return await eor(message, text="Invalid Arguments")

    url = text.split(None, 1)[1]

    try:
        await download(
            url,
            task_id=task_id,
        )
    except Exception as e:
        return await eor(m, text=f"**Error:** `{str(e)}`")

    elapsed = int(time() - start)
    body["Took"] = f"{elapsed}s"

    await eor(m, text=section("Downloaded", body))


@app2.on_message(
    filters.user(SUDOERS)
    & filters.command("upload", prefixes=USERBOT_PREFIX)
)
async def upload_func(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(message, text="Invalid Arguments")

    url_or_path = message.text.split(None, 1)[1]

    start = time()
    task_id = int(start)

    body = {
        "Started": ctime(start),
        "Task ID": task_id,
    }

    m = await eor(message, text=section("Uploading", body))

    async def upload_file(path: str):
        task = await add_task(
            message.reply_document,
            task_id,
            "Uploader",
            path,
        )

        await task
        await rm_task(task_id)

        elapsed = int(time() - start)
        body["Took"] = f"{elapsed}s"

        return await eor(m, text=section("Uploaded", body))

    try:
        if isfile(url_or_path):
            return await upload_file(url_or_path)

        path = await download(
            url_or_path,
            task_id=task_id,
        )

        return await upload_file(path)
    except Exception as e:
        return await eor(m, text=f"**Error:** `{str(e)}`")

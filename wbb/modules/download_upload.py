from os import remove
from os.path import isfile
from time import ctime, time

from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_PREFIX, app2
from wbb.core.sections import section
from wbb.modules.userbot import add_task, eor, rm_task, tasks
from wbb.utils.downloader import download
from wbb.utils.functions import progress


@app2.on_message(
    filters.user(SUDOERS)
    & filters.command("download", prefixes=USERBOT_PREFIX)
)
async def download_func(_, message: Message):
    reply = message.reply_to_message
    start = task_id = int(time())

    if reply:
        m = await eor(message, text="Downloading...")

        task = await add_task(
            reply.download,
            task_id=task_id,
            progress=progress,
            progress_args=(start, task_id, m),
        )
        await task
        await rm_task(task_id)

        elapsed = int(time() - start)
        body = {
            "Started": ctime(start),
            "Time": f"{elapsed}s",
        }
        return await eor(m, text=section("Downloaded", body))

    text = message.text
    if len(text.split()) < 2:
        return await eor(message, text="Invalid Arguments")

    url = text.split(None, 1)[1]
    task_id = int(time())

    body = {
        "Started": ctime(start),
        "Task ID": task_id,
        "URL": url,
    }
    m = await eor(
        message,
        text=section("Downloading", body, underline=False),
        disable_web_page_preview=True,
    )

    try:
        await download(
            url,
            progress_func=(progress, [start, task_id, m]),
            task_id=task_id,
        )
    except Exception as e:
        return await eor(m, text=f"**Error:** `{str(e)}`")

    elapsed = int(time() - start)
    body = {
        "Started": ctime(start),
        "Took": f"{elapsed}s",
        "Task ID": task_id,
    }
    await eor(m, text=section("Downloaded", body, underline=False))


@app2.on_message(
    filters.user(SUDOERS)
    & filters.command("upload", prefixes=USERBOT_PREFIX)
)
async def upload_func(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(message, text="Invalid Arguments")

    url_or_path = message.text.split(None, 1)[1]

    m = await eor(message, text="Uploading..")
    start = task_id = int(time())

    async def upload_file(path):
        task = await add_task(
            message.reply_document,
            task_id,
            path,
            progress=progress,
            progress_args=(start, task_id, m),
        )
        await task
        await rm_task(task_id)
        elapsed = int(time() - start)
        return await eor(m, text=f"Uploaded in {elapsed}s")

    try:
        if isfile(url_or_path):
            return await upload_file(url_or_path)
        path = await download(
            url_or_path,
            task_id=task_id,
            progress_func=(progress, [start, task_id, m]),
        )
        return await upload_file(path)
    except Exception as e:
        return await eor(m, text=f"**Error:** `{str(e)}`")

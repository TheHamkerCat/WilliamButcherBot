from inspect import iscoroutinefunction
from os.path import abspath as absolute_path
from time import time

import aiofiles

from wbb import aiohttpsession as session
from wbb.modules.userbot import add_task, rm_task


def ensure_status(status_code: int):
    if status_code < 200 or status_code >= 300:
        raise Exception(f"HttpProcessingError: {status_code}")


async def download_url(
    url,
    file_path,
    chunk_size,
):
    file_path = file_path or url.split("/")[-1][:20]

    async with session.get(url) as response:
        ensure_status(response.status)

        async with aiofiles.open(file_path, "wb") as f:

            # Save content in file using aiohttp streamReader.
            async for chunk in response.content.iter_chunked(
                chunk_size
            ):
                await f.write(chunk)

    return absolute_path(file_path)


async def download(
    url: str,
    file_path: str = None,
    chunk_size: int = 1000000,  # 1MB chunk
    task_id: int = int(time()),
):
    """
    :url: url where the file is located
    :file_path: path/to/file
    :chunk_size: size of a single chunk
    """
    # Create a task and add it to main tasks dict
    # So we can cancel it using .cancelTask

    task = await add_task(
        download_url,
        task_id,
        "Downloader",
        url=url,
        file_path=file_path,
        chunk_size=chunk_size,
    )
    await task
    await rm_task(task_id)
    return task.result()

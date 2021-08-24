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
    progress_func,
):
    global tasks

    file_path = file_path or url.split("/")[-1][:20]

    progress = 0
    total_size = 0

    # Check if the provided progress function is
    # async for sync in order to call it correctly.
    if progress_func:
        p_f_args = progress_func[1]
        progress_func = progress_func[0]
        is_async = iscoroutinefunction(progress_func)

    # Check if the server responds
    async with session.get(url) as resp:
        ensure_status(resp.status)
        total_size = int(resp.headers["Content-Length"])

    async with session.get(url) as response:
        ensure_status(response.status)

        async with aiofiles.open(file_path, "wb") as f:

            # Save content in file using aiohttp streamReader.
            async for chunk in response.content.iter_chunked(
                chunk_size
            ):
                await f.write(chunk)

                # Call the progress func on each chunk downloaded
                progress += chunk_size
                if progress_func:

                    if is_async:
                        await progress_func(
                            progress, total_size, *p_f_args
                        )
                    else:
                        progress_func(progress, total_size, *p_f_args)

    return absolute_path(file_path)


async def download(
    url: str,
    file_path: str = None,
    chunk_size: int = 1024,
    progress_func=None,
    task_id: int = int(time()),
):
    """
    :url: url where the file is located
    :file_path: path/to/file
    :chunk_size: size of a single chunk
    """
    global tasks

    # Create a task and add it to main tasks dict
    # So we can cancel it using .cancelTask

    task = await add_task(
        download_url,
        task_id,
        url=url,
        file_path=file_path,
        chunk_size=chunk_size,
        progress_func=progress_func,
    )
    await task
    await rm_task(task_id)
    return task.result()

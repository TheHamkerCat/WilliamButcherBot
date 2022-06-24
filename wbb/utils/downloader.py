"""
MIT License

Copyright (c) present TheHamkerCat

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

from os.path import abspath as absolute_path
from time import time

import aiofiles

from wbb import aiohttpsession as session
from wbb.core.tasks import add_task


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
            async for chunk in response.content.iter_chunked(chunk_size):
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

    Returns:
            (asyncio.Task, task_id), With which you can await
            the task, track task progress or cancel it.
    """
    # Create a task and add it to main tasks dict
    # So we can cancel it using .cancelTask

    task, task_id = await add_task(
        download_url,
        "Downloader",
        url=url,
        file_path=file_path,
        chunk_size=chunk_size,
    )

    return task, task_id

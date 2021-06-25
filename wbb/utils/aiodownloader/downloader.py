import asyncio
import os
from typing import Optional

import aiofiles
import aiohttp


class DownloadJob:
    """
    Download Job

    :param file_url: url where the file is located
    :param session: aiohttp session to be used on the job
    :param file_name: name to be used on the file. Defaults to the last part of the url
    :param save_path: dir where the file should be saved. Defaults to the current dir
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        file_url: str,
        save_path: Optional[str] = None,
        chunk_size: Optional[int] = 1024,
    ):

        self.file_url = file_url
        self._session = session
        self._chunk_size = chunk_size

        self.file_name = file_url.split("/")[~0][0:230]
        self.file_path = (
            os.path.join(save_path, self.file_name)
            if save_path
            else self.file_name
        )

        self.completed = False
        self.progress = 0
        self.size = 0

    async def get_size(self) -> int:
        """
        Gets the content-length of the file from the file url.
        :return: the files size in bytes
        """
        if not self.size:
            async with self._session.get(self.file_url) as resp:
                if 200 <= resp.status < 300:
                    self.size = int(resp.headers["Content-Length"])

                else:
                    raise aiohttp.errors.HttpProcessingError(
                        message=f"There was a problem processing {self.file_url}",
                        code=resp.status,
                    )

        return self.size

    def _downloaded(self, chunk_size):
        """
        Method to be called when a chunk of the file is downloaded. It updates the
        progress, adds the size to the _advance variable and checks if the download
        is completed
        """
        self.progress += chunk_size

    async def download(self):
        """
        Downloads the file from the given url to a file in the given path.
        """

        async with self._session.get(self.file_url) as resp:
            # Checkning the response code
            if 200 <= resp.status < 300:
                # Saving the data to the file chunk by chunk.
                async with aiofiles.open(
                    self.file_path, "wb"
                ) as file:

                    # Downloading the file using the aiohttp.StreamReader
                    async for data in resp.content.iter_chunked(
                        self._chunk_size
                    ):
                        await file.write(data)
                        self._downloaded(self._chunk_size)

                self.completed = True
                return self

            else:
                raise aiohttp.errors.HttpProcessingError(
                    message=f"There was a problem processing {self.file_url}",
                    code=resp.status,
                )


class Handler:
    """
    Top level interface with the downloader. It creates the download jobs and handles them.

    :param loop: asyncio loop. if not provided asyncio.get_event_loop() will be used
    :param session: aiohttp session to be used on all downloads. If not provided it will be
    created
    :param chunk_size: chunk bytes sizes to get from the file source. Defaults to 1024 bytes
    """

    def __init__(
        self,
        loop: Optional[asyncio.BaseEventLoop] = None,
        session: Optional[aiohttp.ClientSession] = None,
        chunk_size: Optional[int] = 1024,
    ):

        self._loop = loop or asyncio.get_event_loop()
        self._session = session or aiohttp.ClientSession(
            loop=self._loop
        )
        self._chunk_size = chunk_size

    def _job_factory(
        self, file_url: str, save_path: Optional[str] = None
    ) -> DownloadJob:
        """
        Shortcut for creating a download job. It adds the session and the chunk size.
        :param file_url: url where the file is located
        :param save_path: save path for the download
        :return:
        """
        return DownloadJob(
            self._session, file_url, save_path, self._chunk_size
        )

    async def download(
        self, url: str, save_path: Optional[str] = None
    ) -> DownloadJob:
        """
        Downloads a bulk of files from the given list of urls to the given path.

        :param files_url: list of urls where the files are located
        :param save_path: path to be used for saving the files. Defaults to the current dir
        """

        job = self._job_factory(url, save_path=save_path)

        task = asyncio.ensure_future(job.download())

        await task
        file_name = url.split("/")[-1]
        file_name = (
            file_name[0:230] if len(file_name) > 230 else file_name
        )
        path = (
            os.getcwd() + "/" + file_name
            if not save_path
            else save_path
        )
        return path

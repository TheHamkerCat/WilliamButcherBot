import os
import tempfile

from pyrogram import Client


async def safe_download(client: Client, media, suffix: str = "") -> str:
    """Download media to a random temporary file and return its path."""
    data = await client.download_media(
        media, file_name="download", in_memory=True
    )
    if data is None:
        raise ValueError("Download failed")

    file_descriptor, file_path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(file_descriptor, "wb") as file:
            file.write(data.getvalue())
    except Exception:
        os.remove(file_path)
        raise

    return file_path

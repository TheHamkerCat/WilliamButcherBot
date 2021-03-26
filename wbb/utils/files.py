from PIL import Image
import math

from pyrogram import Client, raw
from pyrogram.file_id import FileId

STICKER_DIMENSIONS = (512, 512)


async def resize_file_to_sticker_size(file_path: str):
    im = Image.open(file_path)
    if (im.width, im.height) < STICKER_DIMENSIONS:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = STICKER_DIMENSIONS[0]/size1
            size1new = STICKER_DIMENSIONS[0]
            size2new = size2 * scale
        else:
            scale = STICKER_DIMENSIONS[1]/size2
            size1new = size1 * scale
            size2new = STICKER_DIMENSIONS[1]
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(STICKER_DIMENSIONS)
    im.save(file_path, "PNG")

async def upload_document(client: Client, file_path: str) -> raw.base.InputDocument:
    media = await client.send(
        raw.functions.messages.UploadMedia(
            peer=raw.types.InputPeerEmpty(),
            media=raw.types.InputMediaUploadedPhoto(
                file=file_path
            )
        )
    )
    return raw.types.InputDocument(id=media.photo.id, access_hash=media.access_hash, file_reference=media.photo.file_reference)

async def get_document_from_file_id(file_id: str) -> raw.base.InputDocument:
    decoded = FileId.decode(file_id)
    return raw.types.InputDocument(id=decoded.media_id, access_hash=decoded.access_hash, file_reference=decoded.file_reference)
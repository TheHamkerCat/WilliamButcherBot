from typing import List

from pyrogram import Client, raw
from pyrogram import errors


async def get_sticker_set_by_name(client: Client, name: str) -> raw.base.messages.StickerSet:
    try:
        return await client.send(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name)
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        return None

# Known errors: (I don't see a reason to catch them as we, for sure, won't face them right now):
# errors.exceptions.bad_request_400.PackShortNameInvalid -> pack name needs to end with _by_botname
# errors.exceptions.bad_request_400.ShortnameOccupyFailed -> pack's name is already in use


async def create_sticker_set(client: Client, owner: int, title: str, short_name: str, stickers: List[raw.base.InputStickerSetItem]) -> raw.base.messages.StickerSet:
    return await client.send(
        raw.functions.stickers.CreateStickerSet(
            user_id=await client.resolve_peer(owner),
            title=title,
            short_name=short_name,
            stickers=stickers
        )
    )


async def add_sticker_to_set(client: Client, stickerset: raw.base.messages.StickerSet, sticker: raw.base.InputStickerSetItem) -> raw.base.messages.StickerSet:
    return await client.send(
        raw.functions.stickers.AddStickerToSet(
            stickerset=raw.types.InputStickerSetShortName(
                short_name=stickerset.set.short_name),
            sticker=sticker
        )
    )


async def create_sticker(sticker: raw.base.InputDocument, emoji: str) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)

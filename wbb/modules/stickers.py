import os
import imghdr
from wbb import app, BOT_USERNAME
from pyrogram import filters
from wbb.utils.errors import capture_err
from wbb.utils.files import resize_file_to_sticker_size, upload_document, get_document_from_file_id
from wbb.utils.stickerset import get_sticker_set_by_name, create_sticker, add_sticker_to_set, create_sticker_set
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, StickerPngNopng, UserIsBlocked

__MODULE__ = "Stickers"
__HELP__ = """/sticker_id - To Get File ID of A Sticker.
/kang - To Kang A Sticker or Image."""

MAX_STICKERS = 120  # would be better if we could fetch this limit directly from telegram
SUPPORTED_TYPES = ['jpeg', 'png', 'webp']


@app.on_message(filters.command("sticker_id") & ~filters.edited)
@capture_err
async def sticker_id(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a sticker.")
        return
    if not message.reply_to_message.sticker:
        await message.reply_text("Reply to a sticker.")
        return
    file_id = message.reply_to_message.sticker.file_id
    await message.reply_text(f"`{file_id}`")


@app.on_message(filters.command("kang") & ~filters.edited)
@capture_err
async def kang(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a sticker/image to kang it.")
        return
    msg = await message.reply_text("Kanging Sticker..")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🤔"

    # Get the corresponding fileid, resize the file if necessary
    doc = (message.reply_to_message.photo or message.reply_to_message.document)
    if message.reply_to_message.sticker:
        sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                    ),
                sticker_emoji
                )
    elif doc:
        temp_file_path = await app.download_media(doc)
        image_type = imghdr.what(temp_file_path)
        if image_type not in SUPPORTED_TYPES:
            await msg.edit("Format not supported! ({})".format(image_type))
            return
        try:
            temp_file_path = await resize_file_to_sticker_size(temp_file_path)
        except OSError as e:
            await msg.edit_text("Something wrong happened.")
            raise Exception(
                f"Something went wrong while resizing the sticker (at {temp_file_path}); {e}")
            return False
        sticker = await create_sticker(
                await upload_document(
                    client,
                    temp_file_path,
                    message.chat.id
                    ),
                sticker_emoji
                )
        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)
    else:
        await msg.edit("Nope, can't kang that.")
        return

    # Find an available pack & add the sticker to the pack; create a new pack if needed
    # Would be a good idea to cache the number instead of searching it every single time...
    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + BOT_USERNAME
    try:
        while True:
            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                        client,
                        message.from_user.id,
                        f"{message.from_user.first_name[:32]}'s kang pack",
                        packname,
                        [sticker]
                        )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = "f" + str(packnum) + "_" + \
                    str(message.from_user.id) + "_by_"+BOT_USERNAME
                continue
            else:
                await add_sticker_to_set(client, stickerset, sticker)
            break

        await msg.edit(
                "Sticker Kanged To [Pack](t.me/addstickers/{})\nEmoji: {}".format(
                    packname,
                    sticker_emoji
                    )
                )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]])
        await msg.edit("Contact Me In Pm First", reply_markup=keyboard)
    except StickerPngNopng:
        await message.reply_text("Stickers must be png files but the provided image was not a png")

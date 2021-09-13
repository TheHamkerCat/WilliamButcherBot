"""
MIT License

Copyright (c) 2021 TheHamkerCat

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
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InputMediaPhoto, InputMediaVideo, Message)

from wbb import app
from wbb.core.decorators.errors import capture_err

# NOTE: THIS MODULE IS SPECIFICALLY FOR @DE_WM GROUP, YOU CAN REMOVE IT IN YOUR FORK IF YOU WANT TO

RICE_GROUP = "DE_WM"
RICE_CHANNEL = "RiceGallery"


@app.on_message(
    filters.chat(RICE_GROUP)
    & (filters.photo | filters.video | filters.document)
    & filters.regex(r"^\[RICE\] ")
    & ~filters.forwarded
    & ~filters.edited
)
@capture_err
async def rice(_, message: Message):
    """Forward media and media_group messages which has caption starts
    with [RICE] with space and description in RICE_GROUP to RICE_CHANNEL
    edited or forwarded messages won't be forwarded
    """
    await message.reply_text(
        "**Waiting for admin to approve...**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Approve (Forward)", callback_data="forward"
                    ),
                    InlineKeyboardButton("Ignore", callback_data="ignore"),
                ]
            ]
        ),
        quote=True,
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("forward"))
async def callback_query_forward_rice(_, callback_query):
    app.set_parse_mode("markdown")
    u_approver = callback_query.from_user
    c_group = callback_query.message.chat
    approver_status = (await c_group.get_member(u_approver.id)).status
    if not (approver_status in ("creator", "administrator")):
        await callback_query.answer("Only admin can approve this!")
        return
    await callback_query.answer("Successfully approved")
    m_op = callback_query.message.reply_to_message
    u_op = m_op.from_user
    arg_caption = f"{m_op.caption}\nOP: [{u_op.first_name}]({m_op.link})"
    if m_op.media_group_id:
        message_id = m_op.message_id
        media_group = await app.get_media_group(RICE_GROUP, message_id)
        arg_media = []
        for m in media_group:
            if m.photo and m.caption:
                arg_media.append(
                    InputMediaPhoto(m.photo.file_id, caption=arg_caption)
                )
            elif m.photo:
                arg_media.append(InputMediaPhoto(m.photo.file_id))
            elif m.video and m.caption:
                arg_media.append(
                    InputMediaVideo(m.video.file_id, caption=arg_caption)
                )
            elif m.video:
                arg_media.append(InputMediaVideo(m.video.file_id))
        m_cp = await app.send_media_group(RICE_CHANNEL, arg_media)
        link = m_cp[0].link
    else:
        m_cp = await m_op.copy(RICE_CHANNEL, caption=arg_caption)
        link = m_cp.link
    await callback_query.message.delete()
    reply_text = (
        f"**OP**: {u_op.mention()}\n"
        f"**Approver**: {u_approver.mention()}\n"
        f"**Forwarded**: [Rice Gallery]({link})"
    )
    await m_op.reply_text(reply_text, disable_web_page_preview=True)


@app.on_callback_query(filters.regex("ignore"))
async def callback_query_ignore_rice(_, callback_query):
    c_group = callback_query.message.chat
    u_disprover = callback_query.from_user
    disprover_status = (await c_group.get_member(u_disprover.id)).status
    m_op = callback_query.message.reply_to_message
    u_op = m_op.from_user
    if u_disprover.id == u_op.id:
        await callback_query.answer("Ok, this rice won't be forwarded")
    elif disprover_status in ("creator", "administrator"):
        await m_op.reply_text(f"{u_disprover.mention} ignored this rice")
    else:
        return await callback_query.answer("Only admin or OP could ignore it")
    await callback_query.message.delete()

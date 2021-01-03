from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from wbb import app

RICE_GROUP = "DE_WM"
RICE_CHANNEL = "RiceGallery"


@app.on_message(filters.chat(RICE_GROUP)
                & filters.media
                & filters.regex(r"^\[RICE\] ")
                & ~filters.forwarded
                & ~filters.edited)
async def rice(_, message: Message):
    """Forward media and media_group messages which has caption starts
    with [RICE] with space and description in RICE_GROUP to RICE_CHANNEL
    edited or forwarded messages won't be forwarded
    """
    await message.reply_text(
        "**Waiting for admin to approve**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Approve (Forward)",
                        callback_data="forward"
                    ),
                    InlineKeyboardButton(
                        "Ignore",
                        callback_data="ignore"
                    )
                ]
            ]
        ),
        quote=True,
        parse_mode="markdown"
    )


@app.on_callback_query(filters.regex("forward"))
async def callback_query_forward_rice(_, callback_query):
    app.set_parse_mode("html")
    approver = callback_query.from_user
    group_chat = callback_query.message.chat
    approver_status = (await group_chat.get_member(approver.id)).status
    if not (approver_status in ("creator", "administrator")):
        await callback_query.answer("Only admin can approve this!")
        return
    await callback_query.answer("Successfully approved")
    m_rice = callback_query.message.reply_to_message
    if m_rice.media_group_id:
        message_id = m_rice.message_id
        media_group = await app.get_media_group(RICE_GROUP, message_id)
        reply = await app.forward_messages(
            RICE_CHANNEL, RICE_GROUP,
            [m.message_id for m in media_group])
        link = reply[0].link
    else:
        reply = await m_rice.forward(RICE_CHANNEL)
        link = reply.link
    await callback_query.message.delete()
    reply_text = (f"<b>OP</b>: {m_rice.from_user.mention()}\n"
                  f"<b>Approver</b>: {approver.mention()}\n"
                  f"<b>Forwarded</b>: "
                  f"<a href=\"{link}\">Rice Gallery</a>")
    await m_rice.reply_text(reply_text, disable_web_page_preview=True)


@app.on_callback_query(filters.regex("ignore"))
async def callback_query_ignore_rice(_, callback_query):
    m_rice = callback_query.message.reply_to_message
    group_chat = callback_query.message.chat
    from_user = callback_query.from_user
    from_user_status = (await group_chat.get_member(from_user.id)).status
    rice_op = callback_query.message.reply_to_message.from_user
    if from_user.id == rice_op.id:
        await callback_query.answer("Ok, this rice won't be forwarded")
    elif from_user_status in ("creator", "administrator"):
        await m_rice.reply_text(f"{from_user.mention} ignored this rice")
    else:
        await callback_query.answer("Only admin or OP could ignore it")
        return
    await callback_query.message.delete()

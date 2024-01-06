#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved
# 
# Modified plugin by @MissKatyPyro from https://github.com/TeamYukki/YukkiAFKBot to make compatible with pyrogram v2
# Re-modified by https://github.com/Hybridvamp for WilliamButcherBot 

import re
import time
import asyncio

from datetime import datetime, timedelta

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from wbb import app, cleanmode
from wbb.utils.filter_groups import afk_group
from wbb.utils.formatter import get_readable_time
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.utils.dbfunctions import add_afk, cleanmode_off, cleanmode_on, is_afk, remove_afk

__MODULE__ = "AFK"
__HELP__ = """/afk [Reason > Optional] - Tell others that you are AFK (Away From Keyboard), so that your boyfriend or girlfriend won't look for you 💔.
/afk [reply to media] - AFK with media.
/afkdel - Enable auto delete AFK message in group (Only for group admin). Default is **Enable**.
Just type something in group to remove AFK Status."""

async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=1),
    }
    cleanmode[chat_id].append(put)

@app.on_message(filters.command("afk"))
@capture_err
async def active_afk(_, message: Message):
    if message.sender_chat:
        msg = await message.reply_text("This feature not supported for channel.")
        await asyncio.sleep(6)
        await msg.delete()
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "animation":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n"
                send = (
                    await message.reply_animation(
                        data,
                        caption=text.format(
                            usr=message.from_user.mention, id=message.from_user.id, tm=seenago
                        ),
                    )
                    if str(reasonafk) == "None"
                    else await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.mention}** [<code>{message.from_user.id}</code>] is back online and was away for {seenago}\n\n**Reason:** `{reasonafk}`\n\n"
                        ),
                    )
            elif afktype == "photo":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n"
                send = (
                    await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=text.format(
                            usr=message.from_user.mention, id=message.from_user.id, tm=seenago
                        ),
                    )
                    if str(reasonafk) == "None"
                    else await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.mention}** [<code>{message.from_user.id}</code>] is back online and was away for {seenago}\n\n**Reason:** `{reasonafk}`\n\n",
                        ),
                    )
            elif afktype == "text":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n"
                send = await message.reply_text(
                    text.format(
                        usr=message.from_user.mention, id=message.from_user.id, tm=seenago
                    ),
                    disable_web_page_preview=True,
                )
            elif afktype == "text_reason":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n**Reason:** `{reas}`\n\n"
                send = await message.reply_text(
                    text.format(
                        usr=message.from_user.mention,
                        id=message.from_user.id,
                        tm=seenago,
                        reas=reasonafk,
                    ),
                    disable_web_page_preview=True,
                )
        except Exception:
            text = "**{usr}** [<code>{id}</code>] is back online"
            send = await message.reply_text(
                text.format(
                    usr=message.from_user.first_name, id=message.from_user.id
                ),
                disable_web_page_preview=True,
            )
        await put_cleanmode(message.chat.id, send.id)
        return
    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.sticker:
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(message.command) > 1 and message.reply_to_message.sticker:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    text = "{usr} [<code>{id}</code>] is now AFK!."
    send = await message.reply_text(
        text.format(usr=message.from_user.mention, id=message.from_user.id)
    )
    await put_cleanmode(message.chat.id, send.id)

@app.on_message(filters.command("afkdel"), group=afk_group)
@adminsOnly("can_change_info")
@capture_err
async def afk_state(_, message: Message):
    if not message.from_user:
        return
    if len(message.command) == 1:
        text = "**Usage:**\n/{cmd} [ENABLE|DISABLE] to enable or disable auto delete message."
        msg = await message.reply_text(text.format(cmd=message.command[0]))
        await asyncio.sleep(6)
        await msg.delete()
        return
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await cleanmode_on(chat_id)
        await message.reply_text("Enabled auto delete AFK message in this chat.")
    elif state == "disable":
        await cleanmode_off(chat_id)
        await message.reply_text("Disabled auto delete AFK message.")
    else:
        text = "**Usage:**\n/{cmd} [ENABLE|DISABLE] to enable or disable auto delete message."
        msg = await message.reply_text(text.format(cmd=message.command[0]))
        await asyncio.sleep(6)
        await msg.delete()

@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=afk_group,
)
@capture_err
async def afk_watcher_func(self: Client, message: Message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.mention
    if message.entities:
        possible = ["/afk", f"/afk@{self.me.username}", "!afk"]
        message_text = message.text or message.caption
        for entity in message.entities:
            try:
                if (
                    entity.type == enums.MessageEntityType.BOT_COMMAND
                    and (message_text[0 : 0 + entity.length]).lower() in possible
                ):
                    return
            except UnicodeDecodeError:  # Some weird character make error
                return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n"
                msg += text.format(
                    usr=user_name, id=userid, tm=seenago
                )
            if afktype == "text_reason":
                text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n**Reason:** `{reas}`\n\n"
                msg += text.format(
                    usr=user_name, id=userid, tm=seenago, reas=reasonafk
                )
            if afktype == "animation":
                if str(reasonafk) == "None":
                    text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n"
                    send = await message.reply_animation(
                        data,
                        caption=text.format(
                            usr=user_name, id=userid, tm=seenago
                        ),
                    )
                else:
                    text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n**Reason:** `{reas}`\n\n"
                    send = await message.reply_animation(
                        data,
                        caption=text.format(
                            usr=user_name, id=userid, tm=seenago, reas=reasonafk
                        ),
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=text.format(
                            usr=user_name, id=userid, tm=seenago
                        ),
                    )
                else:
                    text = "**{usr}** [<code>{id}</code>] is back online and was away for {tm}\n\n**Reason:** `{reas}`\n\n"
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=text.format(
                            usr=user_name, id=userid, tm=seenago, reas=reasonafk
                        ),
                    )
        except:
            text = "**{usr}** [<code>{id}</code>] is back online"
            msg += text.format(usr=user_name, id=userid)

    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = message.reply_to_message.from_user.mention
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time((int(time.time() - timeafk)))
                    if afktype == "text":
                        text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                        msg += text.format(
                            usr=replied_first_name, id=replied_user_id, tm=seenago
                        )
                    if afktype == "text_reason":
                        text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                        msg += text.format(
                            usr=replied_first_name,
                            id=replied_user_id,
                            tm=seenago,
                            reas=reasonafk,
                        )
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                            send = await message.reply_animation(
                                data,
                                caption=text.format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                ),
                            )
                        else:
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                            send = await message.reply_animation(
                                data,
                                caption=text.format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                    reas=reasonafk,
                                ),
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=text.format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                ),
                            )
                        else:
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=text.format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                    reas=reasonafk,
                                ),
                            )
                except Exception as e:
                    await message.reply_text(e)
                    text = "{usr} [<code>{id}</code>] is AFK!."
                    msg += text.format(
                        usr=replied_first_name, id=replied_user_id
                    )
        except:
            pass

    # If username or mentioned user is AFK
    if message.entities:
        entity = message.entities
        j = 0
        for _ in range(len(entity)):
            if (entity[j].type) == enums.MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "text":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                            msg += text.format(
                                usr=user.first_name[:25], id=user.id, tm=seenago
                            )
                        if afktype == "text_reason":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                            msg += text.format(
                                usr=user.first_name[:25],
                                id=user.id,
                                tm=seenago,
                                reas=reasonafk,
                            )
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                                send = await message.reply_animation(
                                    data,
                                    caption=text.format(
                                        usr=user.first_name[:25], id=user.id, tm=seenago
                                    ),
                                )
                            else:
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                                send = await message.reply_animation(
                                    data,
                                    caption=text.format(
                                        usr=user.first_name[:25],
                                        id=user.id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=text.format(
                                        usr=user.first_name[:25], id=user.id, tm=seenago
                                    ),
                                )
                            else:
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=text.format(
                                        usr=user.first_name[:25],
                                        id=user.id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                    except:
                        text = "{usr} [<code>{id}</code>] is AFK!."
                        msg += text.format(
                            usr=user.first_name[:25], id=user.id
                        )
            elif (entity[j].type) == enums.MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "text":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                            msg += text.format(
                                usr=first_name[:25], id=user_id, tm=seenago
                            )
                        if afktype == "text_reason":
                            text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                            msg += text.format(
                                usr=first_name[:25],
                                id=user_id,
                                tm=seenago,
                                reas=reasonafk,
                            )
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                                send = await message.reply_animation(
                                    data,
                                    caption=text.format(
                                        usr=first_name[:25], id=user_id, tm=seenago
                                    ),
                                )
                            else:
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                                send = await message.reply_animation(
                                    data,
                                    caption=text.format(
                                        usr=first_name[:25],
                                        id=user_id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n"
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=text.format(
                                        usr=first_name[:25], id=user_id, tm=seenago
                                    ),
                                )
                            else:
                                text = "**{usr}** [<code>{id}</code>] is AFK since {tm} ago.\n\n**Reason:** {reas}\n\n"
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=text.format(
                                        usr=first_name[:25],
                                        id=user_id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                    except:
                        text = "{usr} [<code>{id}</code>] is AFK!."
                        msg += text.format(usr=first_name[:25], id=user_id)
            j += 1
    if msg != "":
        try:
            send = await message.reply_text(msg, disable_web_page_preview=True)
        except:
            pass
    try:
        await put_cleanmode(message.chat.id, send.id)
    except:
        pass

from wbb import app, arq, IMGBB_API_KEY, MESSAGE_DUMP_CHAT
from wbb.utils.filter_groups import nsfw_detect_group
from wbb.utils.dbfunctions import is_nsfw_on, nsfw_on, nsfw_off
from wbb.modules.admin import member_permissions
from wbb.core.decorators.errors import capture_err
from pyrogram import filters
from random import randint
import aiohttp
import aiofiles
import os


__MODULE__ = "NSFW"
__HELP__ = """
/nsfw_scan - Manually Scan An Image/Sticker/Document.
/anti_nsfw [ENABLE | DISABLE] - Turn This Module On/Off
"""

def calculate_horny(hentai_value, neutral_value, porn_value, sexy_value):
    weight_hentai = 0.18
    weight_neutral = 0.32
    weight_sexy = 0.22
    weight_porn = 0.28
    prominent = max (hentai_value, porn_value, sexy_value)
    if neutral_value < prominent:
        factor_calculation = weight_hentai * hentai_value - weight_neutral * neutral_value + weight_sexy * sexy_value + weight_porn * porn_value
        horny_factor = ((1 - factor_calculation/prominent) * 100)
        return horny_factor
    else: 
        return -1 * neutral_value

@app.on_message((filters.document | filters.photo | filters.sticker) & ~filters.private, group=nsfw_detect_group)
@capture_err
async def detect_nsfw(_, message):
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
    if not await is_nsfw_on(message.chat.id):
        return
    image = await message.download(f"{randint(6666, 9999)}.jpg")
    async with aiofiles.open(image, mode='rb') as f:
        payload = {
            "key": IMGBB_API_KEY,
            "image": await f.read(),
            "expiration": "60"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.imgbb.com/1/upload", data=payload) as resp:
            data = await resp.json()
        try:
            url = data['data']['url']
        except KeyError:
            return
    os.remove(image)
    try:
        results = await arq.nsfw_scan(url)
    except Exception as e:
        print(e)
        return
    hentai = results.data.hentai
    sexy = results.data.sexy
    porn = results.data.porn
    drawings = results.data.drawings
    neutral = results.data.neutral
    hornyfactor = calculate_horny(hentai,neutral,porn,sexy)
    if neutral >= 25:
        return
    if hornyfactor >= 70:
        pass
    elif hornyfactor >= 50:
        # The reason its like this is because later on the plan is to
        # Allow the moderator to decide the maximum allowed nsfw content
        pass
    elif hornyfactor >= 30:
        # This should be okay but still returning True
        # For now only strict checking is implemented
        pass
    else:
        return

    user_mention = message.from_user.mention
    user_id = message.from_user.id
    m = await message.forward(MESSAGE_DUMP_CHAT)
    try:
        await message.delete()
    except Exception:
        pass
    await message.reply_text(f"""
**NSFW [Image]({m.link}) Detected & Deleted Successfully!
————————————————————————**
**User:** {user_mention} [`{user_id}`]
**Safe:** `{neutral} %`
**Porn:** `{porn} %`
**Adult:** `{sexy} %`
**Hentai:** `{hentai} %`
**Drawings:** `{drawings} %`
**————————————————————————**
__Use '/anti_nsfw disable' to disable this.__
""")


@app.on_message(filters.command("nsfw_scan"))
@capture_err
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to an image or document to scan it.")
        return
    reply = message.reply_to_message
    if not reply.document and not reply.photo and not reply.sticker:
        await message.reply_text("Reply to an image/document/sticker to scan it.")
        return
    if message.reply_to_message.document:
        if int(message.reply_to_message.document.file_size) > 3145728:
            return
        mime_type = message.reply_to_message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
    m = await message.reply_text("Scanning")
    image = await message.reply_to_message.download(f"{randint(6666, 9999)}.jpg")
    async with aiofiles.open(image, mode='rb') as f:
        payload = {
            "key": IMGBB_API_KEY,
            "image": await f.read(),
            "expiration": "60"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.imgbb.com/1/upload", data=payload) as resp:
            data = await resp.json()
        try:
            url = data['data']['url']
        except KeyError:
            await m.edit("Failed to upload this to api server.")
    os.remove(image)
    try:
        results = await arq.nsfw_scan(url)
    except Exception as e:
        print(e)
        await m.edit(str(e))
        return
    hentai = results.data.hentai
    sexy = results.data.sexy
    porn = results.data.porn
    drawings = results.data.drawings
    neutral = results.data.neutral
    await m.edit(f"""
**Neutral:** `{neutral} %`
**Porn:** `{porn} %`
**Hentai:** `{hentai} %`
**Sexy:** `{sexy} %`
**Drawings:** `{drawings} %`
""")


@app.on_message(filters.command("anti_nsfw") & ~filters.private)
@capture_err
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /anti_nsfw [enable | disable]")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    user_id = message.from_user.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_change_info" not in permissions:
        await message.reply_text("You don't have enough permissions.")
        return
    if status == "enable":
        await nsfw_on(chat_id)
        await message.reply_text("Enabled AntiNSFW System. I will Delete Messages Containing Inappropriate Content.")
    elif status == "disable":
        await nsfw_off(chat_id)
        await message.reply_text("Disabled AntiNSFW System.")
    else:
        await message.reply_text("Unknown Suffix, Use /anti_nsfw [enable|disable]")

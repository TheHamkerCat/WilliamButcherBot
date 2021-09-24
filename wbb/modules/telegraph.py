import os

from telegraph import upload_file
from pyrogram import filters

from wbb.core.keyboard import ikb
from wbb.core.decorators.errors import capture_err
from wbb import app, tele_graph, BOT_USERNAME

__MODULE__ = "Telegraph"
__HELP__ = """
Upload Media and Paste Documents or Message to Telegra.ph

`/telegraph (reply to a media or text documents or message)`
Reply to Media and Text Documents or Message as args to upload it to Telegraph.

For Custome Title reply with `/telegraph titles`
- Supported Media Types (.jpg, .jpeg, .png, .gif, .mp4)
- Supported Document Text
- Supported Replied To Text Message

For With Command Directly
`/telegraph text ~ title`

For Text Document or Message you can only use Supported HTML Tags from Telegraph
"""

@app.on_message(filters.command(["telegraph", f"telegraph@{BOT_USERNAME}"]))
@capture_err
async def telegraph(_, message):
    reply = message.reply_to_message
    if message.from_user.username:
        uname = f"@{message.from_user.username}"
    else:
        uname = f"{message.from_user.mention}"
    try:
        if reply:
            media = reply.video or reply.photo or reply.animation
            if media:
                if int(media.file_size) < 5242880:
                    file = await reply.download()
                    media_url = upload_file(file)[0]
                    link = f"https://telegra.ph{media_url}"
                    msg = f"**[Here Your Telegra.ph Link!]({link})\n\nUpload by {uname}**"
                    buttons = ikb({"Open Link": link, "Share Link": f"https://telegram.me/share/url?url={link}"}, 2)
                    os.remove(file)
                    return await message.reply_text(msg, quote=True, disable_web_page_preview=True, reply_markup=buttons)
                else:
                    return await message.reply_text("**You can only upload files smaller than 5MB.**", quote=True)
            elif reply.text:
                try:
                    page_name = message.text.split(None, 1)[1]
                except IndexError:
                    page_name = f"Telegraph by @{BOT_USERNAME}"
                text = reply.text.html
                page = tele_graph.create_page(page_name, html_content=text)['url']
                msg = f"**[Here Your Telegra.ph Link!]({page})\n\nPaste by {uname}**"
                buttons = ikb({"Open Link": page, "Share Link": f"https://telegram.me/share/url?url={page}"}, 2)
                return await message.reply_text(msg, quote=True, disable_web_page_preview=True, reply_markup=buttons)
            elif reply.document:
                if int(reply.document.file_size) > 1048576:
                    return await message.reply_text("**You can only paste files smaller than 1MB.**", quote=True)
                if "text" not in reply.document.mime_type:
                    return await message.reply_text("**Only text files can be pasted.**", quote=True)
                file = await reply.download()
                with open(file, "r") as text:
                    text = text.read()
                try:
                    page_name = message.text.split(None, 1)[1]
                except IndexError:
                    page_name = f"Telegraph by @{BOT_USERNAME}"
                page = tele_graph.create_page(page_name, html_content=text)['url']
                msg = f"**[Here Your Telegra.ph Link!]({page})\n\nPaste by {uname}**"
                buttons = ikb({"Open Link": page, "Share Link": f"https://telegram.me/share/url?url={page}"}, 2)
                os.remove(file)
                return await message.reply_text(msg, quote=True, disable_web_page_preview=True, reply_markup=buttons)
        elif not reply and len(message.command) != 1:
            data = message.text.html.split(None, 1)[1]
            msg = data.split(" ~ ")
            text = msg[0]
            if " ~ " in data:
                page_name = msg[-1]
            else:
                page_name = f"Telegraph by @{BOT_USERNAME}"
            page = tele_graph.create_page(page_name, html_content=text)['url']
            msg = f"**[Here Your Telegra.ph Link!]({page})\n\nPaste by {uname}**"
            buttons = ikb({"Open Link": page, "Share Link": f"https://telegram.me/share/url?url={page}"}, 2)
            return await message.reply_text(msg, quote=True, disable_web_page_preview=True, reply_markup=buttons)
        else:
            msg = "**Please Reply to Photo, Video, Text Documents, Message or You can directly with Message too**"
            return await message.reply_text(msg, quote=True)
    except Exception as e:
        return await message.reply_text(str(e), quote=True)

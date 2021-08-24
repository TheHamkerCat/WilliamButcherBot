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

from wbb import BOT_USERNAME, SUDOERS, USERBOT_PREFIX, app2
from wbb.modules.userbot import eor


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & ~filters.edited
    & filters.command("create", prefixes=USERBOT_PREFIX)
)
async def create(_, message):
    if len(message.command) < 3:
        return await eor(message, text="__**.create (b|s|c) Name**__")
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    desc = "Welcome To My " + (
        "Supergroup" if group_type == "s" else "Channel"
    )
    if group_type == "b":  # for basicgroup
        _id = await app2.create_group(group_name, BOT_USERNAME)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Basicgroup Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "s":  # for supergroup
        _id = await app2.create_supergroup(group_name, desc)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Supergroup Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "c":  # for channel
        _id = await app2.create_channel(group_name, desc)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Channel Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )

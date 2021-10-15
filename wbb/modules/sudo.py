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
from pyrogram.types import Message

from wbb import BOT_ID, SUDOERS, USERBOT_PREFIX, app2, eor
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import add_sudo, get_sudoers, remove_sudo
from wbb.utils.functions import restart

__MODULE__ = "Sudo"
__HELP__ = """
**THIS MODULE IS ONLY FOR DEVS**

.useradd - To Add A User In Sudoers.
.userdel - To Remove A User From Sudoers.
.sudoers - To List Sudo Users.

**NOTE:**

Never add anyone to sudoers unless you trust them,
sudo users can do anything with your account, they
can even delete your account.
"""


@app2.on_message(
    filters.command("useradd", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
@capture_err
async def useradd(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to add him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app2.get_users(user_id)).mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await eor(message, text=f"{umention} is already in sudoers.")
    if user_id == BOT_ID:
        return await eor(
            message, text="You can't add assistant bot in sudoers."
        )
    added = await add_sudo(user_id)
    if added:
        await eor(
            message,
            text=f"Successfully added {umention} in sudoers, Bot will be restarted now.",
        )
        return await restart(None)
    await eor(message, text="Something wrong happened, check logs.")


@app2.on_message(
    filters.command("userdel", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
@capture_err
async def userdel(_, message: Message):
    if not message.reply_to_message:
        return await eor(
            message,
            text="Reply to someone's message to remove him to sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    umention = (await app2.get_users(user_id)).mention
    if user_id not in await get_sudoers():
        return await eor(message, text=f"{umention} is not in sudoers.")
    removed = await remove_sudo(user_id)
    if removed:
        await eor(
            message,
            text=f"Successfully removed {umention} from sudoers, Bot will be restarted now.",
        )
        return await restart(None)
    await eor(message, text="Something wrong happened, check logs.")


@app2.on_message(
    filters.command("sudoers", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
@capture_err
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = ""
    for count, user_id in enumerate(sudoers, 1):
        user = await app2.get_users(user_id)
        user = user.first_name if not user.mention else user.mention
        text += f"{count}. {user}\n"
    await eor(message, text=text)

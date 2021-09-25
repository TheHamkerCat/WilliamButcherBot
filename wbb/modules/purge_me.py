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

from wbb import USERBOT_ID, USERBOT_PREFIX, app2, eor, telegraph

__MODULE__ = "Userbot"
TEXT = """
<code>alive</code>  →  Send Alive Message.<br>

<code>create (b|s|c) Title</code>  →  create [basic|super]group & channel<br>

<code>chatbot [ENABLE|DISABLE]</code>  →  Enable chatbot in a chat.<br>

<code>autocorrect [ENABLE|DISABLE]</code>  →  This will autocorrect your messages on the go.<br>

<code>purgeme [Number of messages to purge]</code>  →  Purge your own messages.<br>

<code>eval [Lines of code]</code>  →  Execute Python Code.<br>

<code>lsTasks</code>  →  List running tasks (eval)<br>

<code>sh [Some shell code]</code>  →  Execute Shell Code.<br>

<code>approve</code>  →  Approve a user to PM you.<br>

<code>disapprove</code>  →  Disapprove a user to PM you.<br>

<code>block</code>  →  Block a user.<br>

<code>unblock</code>  →  Unblock a user.<br>

<code>anonymize</code>  →  Change Name/PFP Randomly.<br>

<code>impersonate [User_ID|Username|Reply]</code> → Clone profile of a user.<br>

<code>useradd</code>  →  To add a user in sudoers. [UNSAFE]<br>

<code>userdel</code>  → To remove a user from sudoers.<br>

<code>sudoers</code>  →  To list sudo users.<br>

<code>download [URL or reply to a file]</code>  →  Download a file from TG or URL<br>

<code>upload [URL or File Path]</code>  →  Upload a file from local or URL<br>

<code>parse_preview [REPLY TO A MESSAGE]</code>  →  Parse a web_page(link) preview<br>

<code>id</code>  →  Same as /id but for Ubot<br>

<code>paste</code> → Paste shit on batbin.<br>

<code>help</code> → Get link to this page.<br>

<code>kang</code> → Kang stickers.<br>

<code>dice</code> → Roll a dice.<br>
"""
print("[INFO]: Pasting userbot commands on telegraph")

__HELP__ = f"""**Commands:** {telegraph.create_page(
        "Userbot Commands",
        html_content=TEXT,
    )['url']}"""

print("[INFO]: Done pasting userbot commands on telegraph")


@app2.on_message(
    filters.command("help", prefixes=USERBOT_PREFIX) & filters.user(USERBOT_ID)
)
async def get_help(_, message: Message):
    await eor(
        message,
        text=__HELP__,
        disable_web_page_preview=True,
    )


@app2.on_message(
    filters.command("purgeme", prefixes=USERBOT_PREFIX)
    & filters.user(USERBOT_ID)
)
async def purge_me_func(_, message: Message):
    if len(message.command) != 2:
        return await message.delete()

    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await eor(message, text="Invalid Args")

    n = int(n)

    if n < 1:
        return await eor(message, text="Need a number >=1")

    chat_id = message.chat.id

    message_ids = [
        m.message_id
        async for m in app2.search_messages(
            chat_id,
            from_user=int(USERBOT_ID),
            limit=n,
        )
    ]

    if not message_ids:
        return await eor(message, text="No messages found.")

    # A list containing lists of 100 message chunks
    # because we can't delete more than 100 messages at once,
    # we have to do it in chunks of 100, i'll choose 99 just
    # to be safe.
    to_delete = [
        message_ids[i : i + 99] for i in range(0, len(message_ids), 99)
    ]

    for hundred_messages_or_less in to_delete:
        await app2.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )

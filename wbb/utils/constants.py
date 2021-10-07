# New file

from pyrogram.filters import command, edited
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from wbb import BOT_USERNAME, app

MARKDOWN = """
Read the below text carefully to find out how formatting works!

<u>Supported Fillings:</u>

<code>{name}</code> - This will mention the user with their name.
<code>{chat}</code> - This will fill with the current chat name.

NOTE: Fillings only works in greetings module.


<u>Supported formatting:</u>

<code>**Bold**</code> : Creates <b>bold</b> text.
<code>~~strike~~</code>: Creates <strike>striked</strike> text.
<code>__italic__</code>: Creates <i>italic</i> text.
<code>--underline--</code>: Creates <u>underline</u> text.
<code>`code words`</code>: Creates <code>code words</code> text.
<code>[hyperlink](google.com)</code>: Creates <a href='https://www.google.com'>hyperlink</a> text.
<b>Note:</b> You can use both markdown & html tags.


<u>Button formatting:</u>

-> text ~ [button text, button link]


<u>Example:</u>

<b>example</b> <i>button with markdown</i> <code>formatting</code> ~ [button text, https://google.com]
"""


@app.on_message(command("markdownhelp") & ~edited)
async def mkdwnhelp(_, m: Message):
    keyb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Click Here!",
                    url=f"http://t.me/{BOT_USERNAME}?start=mkdwn_help",
                )
            ]
        ]
    )
    if m.chat.type != "private":
        await m.reply(
            "Click on the below button to get markdown usage syntax in pm!",
            reply_markup=keyb,
        )
    else:
        await m.reply(
            MARKDOWN, parse_mode="html", disable_web_page_preview=True
        )
    return

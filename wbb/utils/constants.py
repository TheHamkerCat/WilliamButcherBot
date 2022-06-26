"""
MIT License

Copyright (c) present TheHamkerCat

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

# New file

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from wbb import BOT_USERNAME, app

MARKDOWN = """
Read the below text carefully to find out how formatting works!

<u>Supported Fillings:</u>

<code>{name}</code> - This will mention the user with their name.
<code>{chat}</code> - This will fill with the current chat name.

NOTE: Fillings only works in greetings module.


<u>Supported formatting:</u>

<code>**Bold**</code> : This will show as <b>bold</b> text.
<code>~~strike~~</code>: This will show as <strike>strike</strike> text.
<code>__italic__</code>: This will show as <i>italic</i> text.
<code>--underline--</code>: This will show as <u>underline</u> text.
<code>`code words`</code>: This will show as <code>code</code> text.
<code>||spoiler||</code>: This will show as <spoiler>Spoiler</spoiler> text.
<code>[hyperlink](google.com)</code>: This will create a <a href='https://www.google.com'>hyperlink</a> text.
<b>Note:</b> You can use both markdown & html tags.


<u>Button formatting:</u>

-> text ~ [button text, button link]


<u>Example:</u>

<b>example</b> <i>button with markdown</i> <code>formatting</code> ~ [button text, https://google.com]
"""


@app.on_message(
    filters.command("markdownhelp")
)
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
    if m.chat.type != enums.ChatType.PRIVATE:
        await m.reply(
            "Click on the below button to get markdown usage syntax in pm!",
            reply_markup=keyb,
        )
    else:
        await m.reply(
            MARKDOWN, 
            parse_mode=enums.ParseMode.HTML, 
            disable_web_page_preview=True
        )
    return

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

from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_PREFIX, app, app2

__MODULE__ = "Dice"
__HELP__ = """
/dice
    Roll a dice.
"""


@app2.on_message(
    filters.command("dice", prefixes=USERBOT_PREFIX) 
    & SUDOERS
)
@app.on_message(
    filters.command("dice")
)
async def throw_dice(client, message: Message):
    six = (message.from_user.id in SUDOERS) if message.from_user else False

    c = message.chat.id
    if not six:
        return await client.send_dice(c, "🎲")

    m = await client.send_dice(c, "🎲")

    while m.dice.value != 6:
        await m.delete()
        m = await client.send_dice(c, "🎲")

from wbb import app, app2
from wbb.utils.errors import capture_err
from pykeyboard import InlineKeyboard
from platform import python_version as pyver
from motor import version as mongover
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton
)


async def alive_function(answers):
    buttons = InlineKeyboard(row_width=1)
    bot_state = 'dead' if not await app.get_me() else 'alive'
    ubot_state = 'dead' if not await app2.get_me() else 'alive'
    buttons.add(InlineKeyboardButton('Stats', callback_data='stats_callback'))
    msg = f"""
**[William✨](https://github.com/thehamkercat/WilliamButcherBot):**
**MainBot:** `{bot_state}`
**UserBot:** `{ubot_state}`
**Pyrogram:** `{pyrover}`
**Python:** `{pyver}`
**MongoDB:** `{mongover}`
"""
    answers.append(
        InlineQueryResultArticle(
            title='Alive',
            description='William ✨',
            input_message_content=InputTextMessageContent(
                msg,
                disable_web_page_preview=True
                ),
            reply_markup=buttons,
            )
        )


@app.on_inline_query()
async def inline_query_handler(client, query):
    answers = []
    await alive_function(answers)

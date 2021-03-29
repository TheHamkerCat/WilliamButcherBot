import sys
from wbb import app, app2, SUDOERS
from wbb.utils.errors import capture_err
from pykeyboard import InlineKeyboard
from sys import version as pyver
from motor import version as mongover
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton
)
""" Inspiration From https://github.com/pokurt/Nana-Remix/blob/master/nana/plugins/assistant/inline_mod/alive.py """


async def alive_function(answers):
    buttons = InlineKeyboard(row_width=1)
    bot_state = 'Dead' if not await app.get_me() else 'Alive'
    ubot_state = 'Dead' if not await app2.get_me() else 'Alive'
    buttons.add(InlineKeyboardButton('Stats', callback_data='stats_callback'))
    msg = f"""
**[William✨](https://github.com/thehamkercat/WilliamButcherBot):**
**MainBot:** `{bot_state}`
**UserBot:** `{ubot_state}`
**Python:** `{pyver.split()[0]}`
**Pyrogram:** `{pyrover}`
**MongoDB:** `{mongover}`
**Platform:** `{sys.platform}`
"""
    answers.append(
        InlineQueryResultArticle(
            title='Alive',
            description="Check Bot's Stats",
            input_message_content=InputTextMessageContent(
                msg,
                disable_web_page_preview=True
                ),
            reply_markup=buttons,
            )
        )
    return answers


@app.on_inline_query()
async def inline_query_handler(client, query):
    answers = []
    answerss = await alive_function(answers)
    await client.answer_inline_query(
        query.id,
        results=answerss,
        switch_pm_text=f'Hello',
        switch_pm_parameter='start',
    )

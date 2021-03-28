from wbb import app
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto


BASE_URL = "https://rgprojectx-gogoanime.herokuapp.com"


RESULT_NUMBER = 0
DATA_LEN = 0
data = None
m = None
initial_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="<<   Previous",
                callback_data="previous"
            ),
            InlineKeyboardButton(
                text="Next   >>",
                callback_data="next"
            )
        ],
        [
            InlineKeyboardButton(
                text="📺   More Details   📺",
                callback_data="more_details"
            )
        ]
    ]
)


@app.on_message(filters.command("anime") & ~filters.edited)
@capture_err
async def anime_search(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Usage:**\n/anime [Query]")
        return
    global RESULT_NUMBER, DATA_LEN, data, m
    RESULT_NUMBER == 0
    m = await message.reply_text("**Searching....**")
    anime_name = message.text.split(None, 1)[1]
    data = await fetch(f"{BASE_URL}/search?name={anime_name}")
    data = data['response']
    DATA_LEN = len(data)
    if DATA_LEN == 0:
        await message.reply_text("**Found literally nothing.**")
        return
    await m.delete()
    m = await app.send_photo(
        message.chat.id,
        photo=data[RESULT_NUMBER]['thumbnail'],
        caption=f"**Title:** {data[RESULT_NUMBER]['title']}",
        reply_markup=initial_keyboard
    )


@app.on_callback_query(filters.regex("previous"))
async def previous_callbacc(_, CallbackQuery):
    global RESULT_NUMBER, data, m
    if RESULT_NUMBER == 0:
        await CallbackQuery.answer(
            "Already On 1st Result, Can't go back.",
            show_alert=True
        )
        return
    RESULT_NUMBER -= 1
    await m.edit_media(media=InputMediaPhoto(data[RESULT_NUMBER]['thumbnail']))
    await m.edit(
        f"**Title:** {data[RESULT_NUMBER]['title']}",
        reply_markup=initial_keyboard
    )


@app.on_callback_query(filters.regex("next"))
async def next_callbacc(_, CallbackQuery):
    global RESULT_NUMBER, DATA_LEN, data, m
    if (RESULT_NUMBER + 1) == DATA_LEN:
        await CallbackQuery.answer(
            "Nothing on the next page.",
            show_alert=True
        )
        return
    RESULT_NUMBER += 1
    await m.edit_media(media=InputMediaPhoto(data[RESULT_NUMBER]['thumbnail']))
    await m.edit(
        f"**Title:** {data[RESULT_NUMBER]['title']}",
        reply_markup=initial_keyboard
    )


@app.on_callback_query(filters.regex("more_details"))
async def more_details_callbacc(_, CallbackQuery):
    global RESULT_NUMBER, data, m
    SLUG = data[RESULT_NUMBER]['slug']
    data = await fetch(f"{BASE_URL}/details?slug={SLUG}")
    data = data['response']
    caption = f"""
**Title:** __{data['title']}__
**Genre:** __{data['genre']}__
**Release:** __{data['release_year']}__
**Status:** __{data['status']}__
**Other Name:** __{data['other_name']}__
**Episodes:** __{len(data['episodes'])}__
**Summary:** __{data['summary']}__"""
    await m.edit_media(media=InputMediaPhoto(data['thumbnail']))
    await m.edit(
        caption,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Delete", callback_data="delete_message")]]))


@app.on_callback_query(filters.regex("delete_message"))
async def delete_callbacc(_, CallbackQuery):
    global RESULT_NUMBER, data, DATA_LEN, m
    RESULT_NUMBER = 0
    data = None
    DATA_LEN = 0
    await m.delete()

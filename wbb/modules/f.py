from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from wbb import app
from pyrogram import filters
from wbb.utils.errors import capture_err

i = 0
m = None
pressers = []
keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("F", callback_data="ff"),
                InlineKeyboardButton("Delete", callback_data="deletef")
                ]
            ]
        )


@app.on_message(filters.command("f"))
@capture_err
async def f(_, message):
    global i, m, pressers
    i = 0
    pressers = []
    try:
        await m.delete()
    except:
        pass
    m = await app.send_message(message.chat.id, text=f"Press F To Pay Respect.\nRespect = `{i}`", reply_markup=keyboard)


@app.on_callback_query(filters.regex("ff"))
async def end_callbacc(_, CallbackQuery):
    global i, m, pressers
    i += 1
    user_id = CallbackQuery.from_user.id
    if user_id in pressers:
        await app.answer_callback_query(CallbackQuery.id,
                "Didn't You Already Pressed 'F' like 0.0069 Seconds Ago?",
                show_alert=True
                )
        return
    pressers.append(user_id)
    await m.edit(text=f"Press F To Pay Respect.\nRespect = `{i}`", reply_markup=keyboard)
    await app.answer_callback_query(CallbackQuery.id, "Respect +", show_alert=True)


@app.on_callback_query(filters.regex("deletef"))
async def del_callbacc(_, CallbackQuery):
    global i, m, pressers
    pressers = []
    i = 0
    await app.send_message(CallbackQuery.message.chat.id, text=f"{CallbackQuery.from_user.id} Deleted F's")
    await m.delete()

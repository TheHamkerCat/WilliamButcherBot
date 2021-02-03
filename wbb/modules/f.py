from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from wbb import app
from pyrogram import filters
from wbb.modules.admin import list_admins
i = 0
m = None
keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("F", callback_data="f"),
                InlineKeyboardButton("Delete", callback_data="delete")
                ]
            ]
        )


@app.on_message(filters.command("f"))
async def f(_, message):
    global i, m
    admins = await list_admins(message.chat.id)
    if message.from_user.id not in admins:
        return
    m = await app.send_message(message.chat.id, text=f"Press F To Pay Respect.\nRespect = `{i}`", reply_markup=keyboard)


@app.on_callback_query(filters.regex("f"))
async def end_callback(_, CallbackQuery):
    global i, m
    i += 1
    await m.edit(text=f"Press F To Pay Respect.\nRespect = `{i}`", reply_markup=keyboard)
    await app.answer_callback_query(
    CallbackQuery.id,
    "Respect +",
    show_alert=True)


@app.on_callback_query(filters.regex("delete"))
async def del_callback(_, CallbackQuery):
    admins = await list_admins(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id not in admins:
        return
    global i, m
    i = 0
    await m.delete()

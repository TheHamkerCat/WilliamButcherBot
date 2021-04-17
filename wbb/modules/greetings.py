""" Kang with proper credits or /gbun """

import asyncio
from wbb import app, WELCOME_DELAY_KICK_SEC, SUDOERS
from wbb.modules.admin import member_permissions
from wbb.utils.errors import capture_err
from wbb.utils.filter_groups import welcome_captcha_group
from wbb.utils.functions import generate_captcha
from wbb.utils.dbfunctions import (
    is_gbanned_user, is_captcha_on, captcha_on, captcha_off
)
from pyrogram.types import (
    Message, InlineKeyboardMarkup,
    InlineKeyboardButton, ChatPermissions, User
)
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, ChatAdminRequired
from pyrogram import filters
from random import shuffle
from datetime import datetime

__MODULE__ = "Captcha"
__HELP__ = "/captcha [ON|OFF] - Enable/Disable Captcha."


answers_dicc = []


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
@capture_err
async def welcome(_, message: Message):
    global answers_dicc
    """Mute new member and send message with button"""
    if not await is_captcha_on(message.chat.id):
        return
    for member in message.new_chat_members:
        try:
            if await is_gbanned_user(member.id):
                await message.chat.kick_member(member.id)
                continue
            if member.is_bot:
                continue  # ignore bots
            if member.id in SUDOERS:
                continue  # ignore sudos
            await message.chat.restrict_member(member.id, ChatPermissions())
            text = (f"Welcome, {(member.mention())} Are you human?\n"
                    f"Solve this captcha in {WELCOME_DELAY_KICK_SEC} seconds or you'll be kicked.")
        except ChatAdminRequired:
            break
        captcha = generate_captcha() # Generate a captcha image, answers and some wrong answers
        captcha_image = captcha[0]
        captcha_answer = captcha[1]
        wrong_answers = captcha[2]  # This consists of 7 wrong answers
        correct_button = InlineKeyboardButton(
            f"{captcha_answer}",
            callback_data=f"pressed_button {captcha_answer} {member.id}"
        )
        temp_keyboard_1 = [correct_button]  # Button row 1
        temp_keyboard_2 = []  # Botton row 2
        for i in range(3):
            temp_keyboard_1.append(
                InlineKeyboardButton(
                    f"{wrong_answers[i]}",
                    callback_data=f"pressed_button {wrong_answers[i]} {member.id}"
                )
            )
        for i in range(3, 7):
            temp_keyboard_2.append(
                InlineKeyboardButton(
                    f"{wrong_answers[i]}",
                    callback_data=f"pressed_button {wrong_answers[i]} {member.id}"
                )
            )
        shuffle(temp_keyboard_1)
        keyboard = [temp_keyboard_1, temp_keyboard_2]
        shuffle(keyboard)
        verification_data = {
            "user_id": member.id,
            "answer": captcha_answer,
            "keyboard": keyboard
        }
        keyboard = InlineKeyboardMarkup(keyboard)
        answers_dicc.append(verification_data)  # Append user info, correct answer and 
                                                # keyboard for later use with callback query
        button_message = await message.reply_photo(
            photo=captcha_image,
            caption=text,
            reply_markup=keyboard,
            quote=True
        )
        asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, button_message, member))
        await asyncio.sleep(0.5)


@app.on_callback_query(filters.regex("pressed_button"))
async def callback_query_welcome_button(_, callback_query):
    """After the new member presses the correct button,
    set his permissions to chat permissions,
    delete button message and join message.
    """
    global answers_dicc
    data = callback_query.data
    pending_user = await app.get_users(int(data.split(None, 2)[2]))
    pressed_user_id = callback_query.from_user.id
    pending_user_id = pending_user.id
    button_message = callback_query.message
    answer = data.split(None, 2)[1]
    if len(answers_dicc) != 0:
        for i in answers_dicc:
            if i['user_id'] == pending_user_id:
                correct_answer = i['answer']
                keyboard = i['keyboard']
    if pending_user_id == pressed_user_id:
        if answer != correct_answer:
            await callback_query.answer("Yeah, It's Wrong.")
            shuffle(keyboard[0])
            shuffle(keyboard[1])
            shuffle(keyboard)
            keyboard = InlineKeyboardMarkup(keyboard)
            await button_message.edit(
                text=button_message.caption.markdown,
                reply_markup=keyboard
            )
            return
        await callback_query.answer("Captcha passed successfully!")
        await button_message.chat.unban_member(pending_user_id)
        await button_message.delete()
        if len(answers_dicc) != 0:
            for ii in answers_dicc:
                if ii['user_id'] == pending_user_id:
                    answers_dicc.remove(ii)
        return
    else:
        await callback_query.answer("This is not for you")
        return


async def kick_restricted_after_delay(delay, button_message: Message, user: User):
    """If the new member is still restricted after the delay, delete
    button message and join message and then kick him
    """
    global answers_dicc
    await asyncio.sleep(delay)
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    user_id = user.id
    await join_message.delete()
    await button_message.delete()
    if len(answers_dicc) != 0:
        for i in answers_dicc:
            if i['user_id'] == user_id:
                answers_dicc.remove(i)
    await _ban_restricted_user_until_date(group_chat, user_id, duration=delay)


async def _ban_restricted_user_until_date(group_chat,
                                          user_id: int,
                                          duration: int):
    try:
        member = await group_chat.get_member(user_id)
        if member.status == "restricted":
            until_date = int(datetime.utcnow().timestamp() + duration)
            await group_chat.kick_member(user_id, until_date=until_date)
    except UserNotParticipant:
        pass


@app.on_message(filters.command("captcha") & ~filters.private)
@capture_err
async def captcha_state(_, message):
    usage = "**Usage:**\n/captcha [ON|OFF]"
    if len(message.command) != 2:
        await message.reply_text(usage)
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_restrict_members" not in permissions:
        await message.reply_text("You don't have enough permissions.")
        return
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await captcha_on(chat_id)
        await message.reply_text("Enabled Captcha For New Users.")
    elif state == "off":
        await captcha_off(chat_id)
        await message.reply_text("Disabled Captcha For New Users.")
    else:
        await message.reply_text(usage)

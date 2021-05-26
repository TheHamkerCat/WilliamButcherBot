import asyncio
from asyncio.exceptions import TimeoutError

from pyrogram import Client, filters
from pyrogram.errors import (PhoneCodeExpired, PhoneCodeInvalid,
                             PhoneNumberInvalid, SessionPasswordNeeded)

from wbb import app
from wbb.core.decorators.errors import capture_err

"""
Credits:
    This module belongs to https://github.com/AbirHasan2005/TG-String-Session/blob/main/genStr.py
"""

__MODULE__ = "GenStr"
__HELP__ = """
This Module Can Be Used To Generate Session String For A Userbot.
Send **/genstr** Command To The Bot In Private And Follow Instructions."""


@app.on_message(filters.command("genstr") & filters.private)
@capture_err
async def genstr(_, message):
    chat = message.chat
    while True:
        number = await app.ask(
            chat.id, "Send Your Phone Number In International Format."
        )
        if not number.text:
            continue
        phone = number.text.strip()
        if phone.startswith("/"):
            continue
        confirm = await app.ask(
            chat.id, f'`Is "{phone}" correct?` \n\nSend: `y`\nSend: `n`'
        )
        if confirm.text.startswith("/"):
            continue
        if "y" in confirm.text.lower():
            break
    try:
        temp_client = Client(
            ":memory:", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        )
    except Exception as e:
        await app.send_message(chat.id, f"**ERROR:** `{str(e)}`")
        return
    try:
        await temp_client.connect()
    except ConnectionError:
        await temp_client.disconnect()
        await temp_client.connect()
    try:
        code = await temp_client.send_code(phone)
        await asyncio.sleep(2)
    except PhoneNumberInvalid:
        return await message.reply_text("Phone Number is Invalid")

    try:
        otp = await app.ask(
            chat.id,
            (
                "An OTP is sent to your phone number, "
                "Please enter OTP in `1 2 3 4 5` format. __(Space between each numbers!)__"
            ),
            timeout=300,
        )

    except TimeoutError:
        return await message.reply_text(
            "Time limit reached of 5 min. Process Cancelled."
        )
    otp_code = otp.text
    try:
        await temp_client.sign_in(
            phone, code.phone_code_hash, phone_code=" ".join(str(otp_code))
        )
    except PhoneCodeInvalid:
        return await message.reply_text("Invalid OTP.")
    except PhoneCodeExpired:
        return await message.reply_text("OTP is Expired.")
    except SessionPasswordNeeded:
        try:
            two_step_code = await app.ask(
                chat.id,
                "Your account have Two-Step Verification.\nPlease enter your Password.",
                timeout=300,
            )
        except TimeoutError:
            return await message.reply_text("Time limit reached of 5 min.")
        new_code = two_step_code.text
        try:
            await temp_client.check_password(new_code)
        except Exception as e:
            return await message.reply_text(f"**ERROR:** `{str(e)}`")
    except Exception as e:
        return await app.send_message(chat.id, f"**ERROR:** `{str(e)}`")
    try:
        session_string = await temp_client.export_session_string()
        await temp_client.disconnect()
        await app.send_message(
            chat.id,
            text=f"**HERE IS YOUR STRING SESSION:**\n```{session_string}```",
        )
    except Exception as e:
        await app.send_message(chat.id, f"**ERROR:** `{str(e)}`")

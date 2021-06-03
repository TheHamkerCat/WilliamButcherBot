"""
MIT License

Copyright (c) 2021 TheHamkerCat

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
import traceback
from io import BytesIO

from googletrans import Translator
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message

from wbb import app

__MODULE__ = "TTS"
__HELP__ = "/tts - Convert Text To Speech."


@app.on_message(filters.command("tts"))
async def text_to_speech(_, message: Message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.text:
                m = await message.reply_text("Processing")
                audio = BytesIO()
                text = message.reply_to_message.text
                i = Translator().translate(text, dest="en")
                lang = i.src
                tts = gTTS(text, lang=lang)
                audio.name = lang + ".mp3"
                tts.write_to_fp(audio)
                await m.delete()
                await message.reply_audio(audio)
                return audio.close()
        await message.reply_text("Reply to some text ffs.")
    except Exception as e:
        await message.reply_text(e)
        e = traceback.format_exc()
        print(e)

from wbb import app, app2
from wbb.utils.errors import capture_err
from pyrogram import filters
import asyncio

__MODULE__ = "RoseFeds"
__HELP__ = "/fbanstat [USERNAME|USER_ID]"

miss_rose = "MissRose_bot"
limit_text = "This command can only be used once every 1 minute."

processing = False


@app.on_message(filters.command("fbanstat"))
@capture_err
async def fbanstat(_, message):
    global processing
    if processing:
        await message.reply_text("One Query Is Already Going On.")
        return
    try:
        processing = True
        if len(message.command) == 2 and not message.reply_to_message:
            user = message.text.strip().split(None, 1)[1]
        elif len(message.command) == 1 and not message.reply_to_message:
            user = message.from_user.id
        elif len(message.command) == 1 and message.reply_to_message:
            user = message.reply_to_message.from_user.id
        else:
            await message.reply_text("**Usage:**\n/fbanstat [USERNAME | USER_ID | REPLY]")
            return
        m = await message.reply_text("**Processing**")
        rose_reply = await app2.ask(miss_rose, f"/fbanstat {user}")
        rose_reply_text = rose_reply.text
        rose_reply_message_id = rose_reply.message_id
        if rose_reply_text.strip() == limit_text:
            await m.edit(limit_text)
            processing = False
            return
        loop_limit = 0
        while True:
            msgg = await app2.get_messages(miss_rose, rose_reply_message_id)
            if msgg.text == rose_reply_text:
                await asyncio.sleep(2)
                if loop_limit > 4:
                    await m.edit(rose_reply_text)
                    processing = False
                    return
                loop_limit += 1
                continue
            rose_reply = msgg.text.markdown
            if "Looks" in rose_reply:
                await m.edit("Too Many Fbans, Rose Sent A "
                             "Fban File, Person Is A Legit Spammer.")
                processing = False
                return
            rose_reply = rose_reply.strip()
            await m.edit(rose_reply)
            processing = False
            return
    except Exception as e:
        processing = False
        await message.reply_text(e)
        return

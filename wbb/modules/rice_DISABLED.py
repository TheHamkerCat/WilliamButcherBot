from wbb import app
from wbb.utils import cust_filter
__MODULE__ = "Rice"
__HELP__ = "/rice - To Forward Your Linux Rice To DE_WM's Rice Gallery"


@app.on_message(filters.chat('de_wm') & cust_filter.command(commands=("rice")))

async def rice(client, message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("```Forwarding!```")
    id = message.reply_to_message.from_user.id
    await message.reply_to_message.forward(-1001490017589)
    await m.edit(
        f"[Your](tg://user?id={id}) Rice Forwared"
        " To [Rice Gallery](https://t.me/RiceGallery)",
        disable_web_page_preview=True
    )

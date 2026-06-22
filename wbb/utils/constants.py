# New file

from pyrogram.enums import ChatType, ParseMode
from pyrogram.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from wbb import BOT_USERNAME, app

MARKDOWN = """
اقرأ النص أدناه بعناية لمعرفة كيفية عمل التنسيق!

<u>الوسوم المدعومة:</u>

<code>{name}</code> - سيذكر المستخدم باسمه.
<code>{chat}</code> - سيُعبّأ باسم المحادثة الحالية.

ملاحظة: الوسوم تعمل فقط في وحدة رسائل الترحيب.


<u>التنسيق المدعوم:</u>

<code>**عريض**</code> : سيظهر كنص <b>عريض</b>.
<code>~~مشطوب~~</code>: سيظهر كنص <strike>مشطوب</strike>.
<code>__مائل__</code>: سيظهر كنص <i>مائل</i>.
<code>--تحته خط--</code>: سيظهر كنص <u>تحته خط</u>.
<code>`كود`</code>: سيظهر كنص <code>كود</code>.
<code>||مخفي||</code>: سيظهر كنص <spoiler>مخفي</spoiler>.
<code>[رابط](google.com)</code>: سيُنشئ نصاً <a href='https://www.google.com'>كرابط</a>.
<b>ملاحظة:</b> يمكنك استخدام كلٍّ من markdown وعلامات html.


<u>تنسيق الأزرار:</u>

-> نص ~ [نص الزر, رابط الزر]


<u>مثال:</u>

<b>مثال</b> <i>زر مع markdown</i> <code>تنسيق</code> ~ [نص الزر, https://google.com]
"""


@app.on_message(command("markdownhelp"))
async def mkdwnhelp(_, m: Message):
    keyb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="اضغط هنا!",
                    url=f"http://t.me/{BOT_USERNAME}?start=mkdwn_help",
                )
            ]
        ]
    )
    if m.chat.type != ChatType.PRIVATE:
        await m.reply(
            "اضغط على الزر أدناه للحصول على توضيح صياغة الماركداون في الخاص!",
            reply_markup=keyb,
        )
    else:
        await m.reply(
            MARKDOWN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
    return

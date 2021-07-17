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
from .functions import button_parser


async def get_msg_file(message):
    reply = message.reply_to_message
    _type = None
    file_id = None
    text = ""
    buttons = []
    if not reply:
        args = message.text.markdown.split(" ", 2)
        text, buttons = button_parser(args[2])
        _type = "button_text" if buttons else "text"
    elif reply:
        if txt := reply.text or reply.caption:
            text, buttons = button_parser(txt.markdown)
        if reply.text:
            _type = "button_text" if buttons else "text"
        elif sticker := reply.sticker:
            file_id = sticker['file_id']
            _type = "sticker"
        elif animation := reply.animation:
            file_id = animation['file_id']
            _type = "animation"
        elif photo := reply.photo:
            file_id = photo['file_id']
            _type = "photo"
        elif document := reply.document:
            file_id = document['file_id']
            _type = "document"
        elif video := reply.video:
            file_id = video['file_id']
            _type = "video"
        elif audio := reply.audio:
            file_id = audio['file_id']
            _type = "audio"
        elif video_note := reply.video_note:
            file_id = video_note['file_id']
            _type = "video_note"
        elif voice := reply.voice:
            file_id = voice['file_id']
            _type = "voice"
    else:
        return
    return text, _type, file_id, buttons
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
from typing import List, Optional, Union

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import DOCUMENT_TYPES, PHOTO_TYPES, FileId, FileType
from pyrogram.types import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):
    """Link to an audio.
    By default, this audio will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message
    with the specified content instead of the audio.
    Parameters:
        audio_url (``str``):
            A valid URL for the embedded audio player or audio file.

        thumb_url (``str``):
            URL of the thumbnail (jpeg only) for the audio.

        title (``str``):
            Title for the result.

        mime_type (``str``):
            Mime type of the content of audio url, “text/html” or “audio/mp3”.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters.

        performer (``str``, *optional*):
            Performer.

        duration (``int``, *optional*):
            Audio duration in seconds.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the audio. This field is required if InlineQueryResultAudio is
            used to send an HTML-page as a result.
    """

    def __init__(
        self,
        audio_url: str,
        thumb_url: str,
        title: str,
        mime_type: str,
        id: str = None,
        description: str = None,
        caption: str = "",
        performer: str = "",
        duration: int = 0,
        parse_mode: Optional[str] = object,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_url = audio_url
        self.thumb_url = thumb_url
        self.voice = bool(mime_type == "audio/ogg")
        self.title = title
        self.caption = caption
        self.description = description
        self.mime_type = mime_type
        self.parse_mode = parse_mode
        self.performer = performer
        self.duration = duration
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

        if mime_type == "text/html" and input_message_content is None:
            raise ValueError(
                "input_message_content is required for audio with `text/html` mime type"
            )

    async def write(self, client: "pyrogram.Client"):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[],
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[
                raw.types.DocumentAttributeAudio(
                    duration=self.duration,
                    voice=self.voice,
                    title=self.title,
                    performer=self.performer,
                )
            ],
        )

        message, entities = (
            await utils.parse_text_entities(
                client,
                self.caption,
                self.parse_mode,
                self.caption_entities,
            )
        ).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=audio,
            send_message=(
                await self.input_message_content.write(
                    client, self.reply_markup
                )
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                    message=message,
                    entities=entities,
                )
            ),
        )


#  CREDITS:
#       THE CODE BELOW THIS LINE IS WRITTEN BY https://github.com/Mahesh0253. [https://t.me/DeletedUser420]
#       https://github.com/Mahesh0253/pyrogram/blob/inline/pyrogram/types/inline_mode/inline_query_result_cached_document.py


class InlineQueryResultCachedDocument(InlineQueryResult):
    """Link to a file stored on the Telegram servers.

    By default, this file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content instead of the file.

    Parameters:
        title (``str``):
            Title for the result.

        file_id (``str``):
            Pass a file_id as string to send a media that exists on the Telegram servers.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent.
    """

    def __init__(
        self,
        file_id: str,
        title: str = None,
        id: str = None,
        description: str = None,
        caption: str = "",
        parse_mode: Optional[str] = object,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
    ):
        super().__init__("file", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self, client: "pyrogram.Client"):
        document = get_input_file_from_file_id(self.file_id)

        message, entities = (
            await utils.parse_text_entities(
                client,
                self.caption,
                self.parse_mode,
                self.caption_entities,
            )
        ).values()

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            document=document,
            send_message=(
                await self.input_message_content.write(
                    client, self.reply_markup
                )
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                    message=message,
                    entities=entities,
                )
            ),
        )


def get_input_file_from_file_id(
    file_id: str, expected_file_type: FileType = None
) -> Union["raw.types.InputPhoto", "raw.types.InputDocument"]:
    try:
        decoded = FileId.decode(file_id)
    except Exception:
        raise ValueError(
            f'Failed to decode "{file_id}". The value does not represent an existing local file, '
            f"HTTP URL, or valid file id."
        )

    file_type = decoded.file_type

    if expected_file_type is not None and file_type != expected_file_type:
        raise ValueError(
            f'Expected: "{expected_file_type}", got "{file_type}" file_id instead'
        )

    if file_type in (FileType.THUMBNAIL, FileType.CHAT_PHOTO):
        raise ValueError(
            f"This file_id can only be used for download: {file_id}"
        )

    if file_type in PHOTO_TYPES:
        return raw.types.InputPhoto(
            id=decoded.media_id,
            access_hash=decoded.access_hash,
            file_reference=decoded.file_reference,
        )

    if file_type in DOCUMENT_TYPES:
        return raw.types.InputDocument(
            id=decoded.media_id,
            access_hash=decoded.access_hash,
            file_reference=decoded.file_reference,
        )

    raise ValueError(f"Unknown file id: {file_id}")

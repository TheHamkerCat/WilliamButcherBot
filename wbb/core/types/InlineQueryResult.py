#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, List, Union
import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import FileType
from pyrogram.parser import Parser
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

        voice (``bool``, *optional*):
            True if the audio is a voice note, defaults to False.

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
        voice: bool = False,
        description: str = None,
        caption: str = "",
        performer: str = "",
        duration: int = 0,
        parse_mode: Optional[str] = object,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_url = audio_url
        self.thumb_url = thumb_url
        self.voice = voice
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
            raise ValueError("input_message_content is required for audio with `text/html` mime type")


    async def write(self, client: "pyrogram.Client"):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[]
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[raw.types.DocumentAttributeAudio(
                duration=self.duration,
                voice=self.voice,
                title=self.title,
                performer=self.performer,
            )]
        )

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=audio,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities)
            )
        )


class InlineQueryResultCachedAudio(InlineQueryResult):
    """Represents a link to an MP3 audio file stored on the Telegram servers.

    By default, this audio file will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.    
    
    Parameters:
        file_id (``str``):
            A valid file identifier for the audio file
            
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
            
        caption (``str``, *optional*):
            Caption, 0-1024 characters after entities parsing.

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
        id: str = None,
        caption: str = "",
        parse_mode: Optional[str] = object,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


    async def write(self, client: "pyrogram.Client"):
        audio = utils.get_input_media_from_file_id(self.file_id, FileType.AUDIO)

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()
        print(audio)
        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            document=audio,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )

""" WRITTEN BY @pokurt, https://github.com/pokurt"""

import sys
import traceback
from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from wbb import LOG_GROUP_ID, app


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await app.send_message(LOG_GROUP_ID, x)
            raise err

    return capture

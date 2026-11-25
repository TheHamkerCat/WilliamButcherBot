"""
MIT License

Copyright (c) 2024 TheHamkerCat

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
import subprocess
import tempfile
from os import path

from pyrogram import enums, filters
from pyrogram.types import Message

from wbb import MONGO_URL, SUDOERS, app


@app.on_message(filters.command("backup") & SUDOERS)
async def backup(_, message: Message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply("This command can only be used in private")

    m = await message.reply("Backing up data...")

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            dump = subprocess.run(
                ["mongodump", "--uri", MONGO_URL],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            return await m.edit(
                "mongodump is not installed. Install mongo-database-tools "
                + "from mongodb.com/try/download/database-tools"
            )
        if dump.returncode != 0:
            return await m.edit(
                "Looks like you don't have mongo-database-tools installed "
                + "grab it from mongodb.com/try/download/database-tools"
            )

        try:
            archive = subprocess.run(
                ["zip", "-r", "-9", "backup.zip", "dump"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            return await m.edit("`zip` is not installed, BACKUP FAILED!")
        if archive.returncode != 0:
            return await m.edit(
                "Looks like you don't have `zip` package installed, BACKUP FAILED!"
            )

        await message.reply_document(path.join(temp_dir, "backup.zip"))

    await m.delete()

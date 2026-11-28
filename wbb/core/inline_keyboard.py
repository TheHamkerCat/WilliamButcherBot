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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboard(InlineKeyboardMarkup):
    """Inline keyboard that splits buttons into rows of row_width."""

    def __init__(self, row_width: int = 3):
        super().__init__(inline_keyboard=[])
        self.row_width = row_width

    def add(self, *buttons: InlineKeyboardButton):
        # Replaces any rows that were added before
        self.inline_keyboard = [
            list(buttons[start : start + self.row_width])
            for start in range(0, len(buttons), self.row_width)
        ]

    def row(self, *buttons: InlineKeyboardButton):
        self.inline_keyboard.append(list(buttons))

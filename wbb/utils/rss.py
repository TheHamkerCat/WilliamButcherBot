"""
MIT License

Copyright (c) present TheHamkerCat

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

class Feed:
    def __init__(self, feed):
        if not feed.get("entries"):
            return
        entry = feed["entries"][0]
        self.title = entry.get("title") or ""

        # We need title to check latest post
        if not self.title:
            return

        self.link = entry.get("link") or ""
        self.published = entry.get("published") or ""
        self.updated = entry.get("updated") or ""
        self.author = entry.get("author")
        self.summary = entry.get("summary") or ""

    def parsed(self):
        text = f"**Title:** [{self.title.strip()}]({self.link or 'https://google.com'})\n"
        if self.author:
            text += f"**Author:** {self.author}\n"
        if self.published:
            text += f"**Published:** `{self.published}`\n"
        if self.updated:
            text += f"**Last Updated:** `{self.updated}`\n"

        if self.summary and "<div" not in self.summary:
            text += f"**Summary:** {self.summary.strip()}\n"

        if text:
            return "\n".join([i.strip() for i in text.splitlines()])

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
        text = (
            f"**Title:** [{self.title.strip()}]({self.link or 'https://google.com'})\n"
        )
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

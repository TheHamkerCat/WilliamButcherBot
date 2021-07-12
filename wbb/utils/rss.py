from feedparser import parse


class Feed:
    def __init__(self, url: str):
        self.url = url
        feed = parse(url)
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
        text = ""
        if self.title:
            text += f"**Title:** {self.title}\n"
        if self.author:
            text += f"**Author:** {self.author}\n"
        if self.link:
            text += f"**Link:** {self.link}\n"
        if self.updated:
            text += f"**Last Updated:** {self.updated}\n"
        if self.published:
            text += f"**Published:** {self.published}\n"
        if self.summary:
            if "<div" not in self.summary:
                text += f"**Summary:** {self.summary}\n"

        if text:
            text = "\n".join([i.strip() for i in text.splitlines()])
        return text

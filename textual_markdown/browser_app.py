from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult

from .widgets import MarkdownBrowser


class BrowserApp(App):
    def compose(self) -> ComposeResult:
        yield MarkdownBrowser()

    async def on_mount(self) -> None:
        await self.load("README.md")

    async def load(self, path: str) -> None:
        markdown = Path(path).read_text()
        browser = self.query_one(MarkdownBrowser)
        await browser.document.update(markdown)


if __name__ == "__main__":
    app = BrowserApp()
    app.run()

from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer

from .widgets import MarkdownBrowser


class BrowserApp(App):
    BINDINGS = [("t", "toggle_toc", "TOC")]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield MarkdownBrowser()

    async def on_mount(self) -> None:
        await self.load("README.md")
        self.query_one(MarkdownBrowser).focus()

    async def load(self, path: str) -> None:
        markdown = Path(path).read_text()
        browser = self.query_one(MarkdownBrowser)
        await browser.document.update(markdown)

    def action_toggle_toc(self) -> None:
        browser = self.query_one(MarkdownBrowser)
        browser.show_toc = not browser.show_toc


if __name__ == "__main__":
    app = BrowserApp()
    app.run()

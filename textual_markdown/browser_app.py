from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer

from .widgets import MarkdownBrowser


class BrowserApp(App):
    BINDINGS = [
        ("t", "toggle_toc", "TOC"),
        ("b", "back", "Back"),
        ("f", "forward", "Forward"),
    ]

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Footer()
        yield MarkdownBrowser()

    @property
    def browser(self) -> MarkdownBrowser:
        return self.query_one(MarkdownBrowser)

    async def on_mount(self) -> None:
        self.browser.document.focus()
        if not await self.browser.go(self.path):
            self.exit(message=f"Unable to load {self.path!r}")

    async def load(self, path: str) -> None:
        await self.browser.go(path)

    def action_toggle_toc(self) -> None:
        self.browser.show_toc = not self.browser.show_toc

    async def action_back(self) -> None:
        await self.browser.back()

    async def action_forward(self) -> None:
        await self.browser.forward()


if __name__ == "__main__":
    app = BrowserApp()
    app.run()

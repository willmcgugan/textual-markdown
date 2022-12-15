from __future__ import annotations

from typing import TypeAlias

from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Tree


from markdown_it import MarkdownIt


TOC: TypeAlias = "list[tuple[int, str, str]]"


class TOCUpdated(Message, bubble=True):
    def __init__(self, toc: TOC, *, sender: Widget) -> None:
        super().__init__(sender=sender)
        self.toc = toc


class TOCSelected(Message, bubble=True):
    def __init__(self, block_id: str, *, sender: Widget) -> None:
        super().__init__(sender=sender)
        self.block_id = block_id


class Block(Static):
    DEFAULT_CSS = """
    Block {
        height: auto;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        self.blocks: list[Block] = []
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield from self.blocks
        self.blocks.clear()


class Header(Block):
    DEFAULT_CSS = """
    Header {
        color: $text;
    }
    """


class H1(Header):
    DEFAULT_CSS = """
    
    H1 {
        background: $accent-darken-2;
        border: wide $background;
        content-align: center middle;
        padding: 1;
        text-style: bold;
        color: $text;
    }
    
    """


class H2(Header):
    DEFAULT_CSS = """
    
    H2 {
        background: $panel;
        border: wide $background;
        text-align: center;
        text-style: underline;
        color: $text;
        padding: 1 0;
        text-style: bold;
    }
    
    """


class H3(Header):

    DEFAULT_CSS = """
    H3 {
        background: $panel;
        text-style: bold;
        color: $text;
        margin: 1 0;
    }
    """


class H4(Header):
    DEFAULT_CSS = """
    H4 {
        text-style: underline;
        padding: 1 0;
    }
    
    """


class H5(Header):
    DEFAULT_CSS = """
    H5 {
        text-style: bold;
        color: $text;
        padding: 1 0;
    }
    
    """


class H6(Header):
    DEFAULT_CSS = """
    H5 {
        text-style: bold;
        color: $text-muted;
        padding: 1 0;
    }
    
    """


class Paragraph(Block):
    pass


class BlockQuote(Block):
    DEFAULT_CSS = """
    BlockQuote { 
        background: $boost;
        border-left: outer $success;
        margin: 1 0;
        padding: 0 1;
    }
    BlockQuote > BlockQuote {
        margin-left: 2;
        margin-top: 1;
    }
    
    """


class Fence(Block):
    DEFAULT_CSS = """
    Fence {
        margin: 1 0;
        overflow: auto;
        width: 100%;
    }

    Fence > * {
        width: auto;
    }
    """

    def __init__(self, code: str, lexer: str) -> None:
        self.code = code
        self.lexer = lexer
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(
            Syntax(
                self.code,
                lexer=self.lexer,
                word_wrap=False,
                indent_guides=True,
                padding=(1, 2),
                theme="material",
            ),
            expand=True,
            shrink=False,
        )


HEADINGS = {"h1": H1, "h2": H2, "h3": H3, "h4": H4, "h5": H5, "h6": H6}


class MarkdownDocument(Widget):
    DEFAULT_CSS = """
    MarkdownDocument {
        height: auto;
        margin: 0 4;        
    }
    """

    async def update(self, markdown: str) -> None:
        output: list[Block] = []
        stack: list[Block] = []
        parser = MarkdownIt("gfm-like")

        content = Text()
        block_id: int = 0

        toc: TOC = []

        for token in parser.parse(markdown):
            self.log(token)
            if token.type == "heading_open":
                block_id += 1
                stack.append(HEADINGS[token.tag](id=f"block{block_id}"))

            elif token.type == "paragraph_open":
                stack.append(Paragraph())
            elif token.type == "blockquote_open":
                stack.append(BlockQuote())
            elif token.type.endswith("_close"):

                block = stack.pop()
                if token.type == "heading_close":
                    heading = block.render().plain
                    level = int(token.tag[1:])
                    toc.append((level, heading, block.id))

                if stack:
                    stack[-1].blocks.append(block)
                else:
                    output.append(block)
            elif token.type == "inline":
                style_stack: list[Style] = [Style()]
                content = Text()
                if token.children:
                    for child in token.children:
                        if child.type == "text":
                            content.append(child.content, style_stack[-1])
                        elif child.type == "em_open":
                            style_stack.append(style_stack[-1] + Style(italic=True))
                        elif child.type == "em_close":
                            style_stack.pop()
                stack[-1].update(content)
            elif token.type == "fence":
                output.append(
                    Fence(
                        token.content.rstrip(),
                        token.info,
                    )
                )

        await self.emit(TOCUpdated(toc, sender=self))
        await self.mount(*output)


class MarkdownTOC(Widget):
    DEFAULT_CSS = """
    MarkdownTOC {
        width: 32;
        background: $panel;
        border-right: wide $background;
    }
    MarkdownTOC > Tree {
        padding: 1;
        width: 100%;
    }
    """

    toc: reactive[TOC | None] = reactive(None, init=False)

    def compose(self) -> ComposeResult:
        tree = Tree("TOC")
        tree.show_root = False
        tree.show_guides = False
        tree.guide_depth = 2
        tree.auto_expand = False
        yield tree

    def watch_toc(self, toc: TOC) -> None:
        self.set_toc(toc)

    def set_toc(self, toc: TOC) -> None:
        tree = self.query_one(Tree)
        root = tree.root
        for level, name, block_id in toc:
            node = root
            for _ in range(level - 1):
                if node._children:
                    node.expand()
                    node.allow_expand = True
                    node = node._children[-1]
                else:
                    node = node.add(str(level), expand=True)
            node.add_leaf(name, {"block_id": block_id})

    async def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        await self.emit(TOCSelected(message.node.data["block_id"], sender=self))


class MarkdownBrowser(Vertical):
    DEFAULT_CSS = """
    MarkdownBrowser {
        height: 1fr;
        scrollbar-gutter: stable;
    }

    MarkdownTOC {
        dock:left;
    }
    
    MarkdownBrowser > MarkdownTOC {        
        display: none;
    }
    
    MarkdownBrowser.-show-toc > MarkdownTOC {
        display: block;
    }
    
    
    """

    show_toc = reactive(True)
    top_block = reactive("")

    @property
    def document(self) -> MarkdownDocument:
        return self.query_one(MarkdownDocument)

    def watch_show_toc(self, show_toc: bool) -> None:
        self.set_class(show_toc, "-show-toc")

    def compose(self) -> ComposeResult:
        yield MarkdownTOC()
        yield MarkdownDocument()

    def on_tocupdated(self, message: TOCUpdated) -> None:
        self.query_one(MarkdownTOC).toc = message.toc
        message.stop()

    def on_tocselected(self, message: TOCSelected) -> None:
        block_selector = f"#{message.block_id}"
        block = self.query_one(block_selector, Block)
        self.scroll_to_widget(block, top=True)
        message.stop()

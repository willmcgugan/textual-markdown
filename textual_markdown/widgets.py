from __future__ import annotations

from pathlib import Path
from typing import Iterable, TypeAlias

from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive, var
from textual.widget import Widget
from textual.widgets import Static, Tree
from textual.widgets import DataTable

from markdown_it import MarkdownIt

from .navigator import Navigator

TOC: TypeAlias = "list[tuple[int, str, str]]"


class TOCUpdated(Message, bubble=True):
    def __init__(self, toc: TOC, *, sender: Widget) -> None:
        super().__init__(sender=sender)
        self.toc = toc


class TOCSelected(Message, bubble=True):
    def __init__(self, block_id: str, *, sender: Widget) -> None:
        super().__init__(sender=sender)
        self.block_id = block_id


class LinkClicked(Message, bubble=True):
    def __init__(self, href: str, *, sender: Widget) -> None:
        super().__init__(sender=sender)
        self.href = href


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

    def set_content(self, text: Text) -> None:
        self.update(text)

    async def action_link(self, href: str) -> None:
        await self.emit(LinkClicked(href, sender=self))


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
        padding: 1;
        text-style: bold;
    }
    
    """


class H3(Header):

    DEFAULT_CSS = """
    H3 {
        background: $surface;
        text-style: bold;
        color: $text;        
        border-bottom: wide $foreground;
        width: auto;
    }
    """


class H4(Header):
    DEFAULT_CSS = """
    H4 {
        text-style: underline;
        margin: 1 0;
    }
    
    """


class H5(Header):
    DEFAULT_CSS = """
    H5 {
        text-style: bold;
        color: $text;
        margin: 1 0;
    }
    
    """


class H6(Header):
    DEFAULT_CSS = """
    H6 {
        text-style: bold;
        color: $text-muted;
        margin: 1 0;
    }
    
    """


class Paragraph(Block):
    DEFAULT_CSS = """
    MarkdownDocument > Paragraph {
         margin: 0 0 1 0;
    }
    """


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


class BulletList(Block):
    DEFAULT_CSS = """
    
    BulletList {
        margin: 0;
        padding: 0 0;
    }

    BulletList BulletList {
        margin: 0;
        padding-top: 0;
    }
    
    """


class OrderedList(Block):
    DEFAULT_CSS = """
    
    OrderedList {
        margin: 0;
        padding: 0 0;
    }

    OrderedList OrderedList {
        margin: 0;
        padding-top: 0;
    }
    
    """


class Table(Block):
    DEFAULT_CSS = """
    Table {
        margin: 1 0;
    }
    Table > DataTable {        
        width: 100%;
        height: auto;                
    }
    """

    def compose(self) -> ComposeResult:
        def flatten(block: Block) -> Iterable[Block]:
            for block in block.blocks:
                if block.blocks:
                    yield from flatten(block)
                yield block

        headers: list[Text] = []
        rows: list[list[Text]] = []
        for block in flatten(self):
            if isinstance(block, TH):
                headers.append(block.render())
            elif isinstance(block, TR):
                rows.append([])
            elif isinstance(block, TD):
                rows[-1].append(block.render())

        table = DataTable(zebra_stripes=True)
        table.can_focus = False
        table.add_columns(*headers)
        table.add_rows([row for row in rows if row])
        yield table
        self.blocks.clear()


class TBody(Block):
    DEFAULT_CSS = """
    
    """


class THead(Block):
    DEFAULT_CSS = """
    
    """


class TR(Block):
    DEFAULT_CSS = """
    
    """


class TH(Block):
    DEFAULT_CSS = """
    
    """


class TD(Block):
    DEFAULT_CSS = """
    
    """


class Bullet(Widget):
    DEFAULT_CSS = """
    Bullet {
        width: auto;
    }
    """

    symbol = reactive("●​ ")

    def render(self) -> Text:
        return Text(self.symbol)


class ListItem(Block):
    DEFAULT_CSS = """
    
    ListItem {
        layout: horizontal;
        margin-right: 1;
        height: auto;
    }

    ListItem > Vertical {
        width: 1fr;
        height: auto;       
    }
    
    """

    def __init__(self, bullet: str) -> None:
        self.bullet = bullet
        super().__init__()

    def compose(self) -> ComposeResult:

        bullet = Bullet()
        bullet.symbol = self.bullet
        yield bullet
        yield Vertical(*self.blocks)

        self.blocks.clear()


class Fence(Block):
    DEFAULT_CSS = """
    Fence {
        margin: 1 0;
        overflow: auto;
        width: 100%;
        height: auto;
        max-height: 20;        
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

NUMERALS = " ⅠⅡⅢⅣⅤⅥ"


class MarkdownDocument(Widget):
    DEFAULT_CSS = """
    MarkdownDocument {
        height: auto;
        margin: 0 4 1 4;
        layout: vertical;        
    }
    .em {
        text-style: italic;
    }
    .strong {
        text-style: bold;
    }
    .s {
        text-style: strike;
    }
    .code_inline {
        text-style: bold dim;                       
    }
    """
    COMPONENT_CLASSES = {"em", "strong", "s", "code_inline"}

    async def load(self, path: Path) -> bool:
        try:
            markdown = path.read_text()
        except Exception:
            return False
        await self.query("Block").remove()
        await self.update(markdown)
        return True

    async def update(self, markdown: str) -> None:
        output: list[Block] = []
        stack: list[Block] = []
        parser = MarkdownIt("gfm-like")

        content = Text()
        block_id: int = 0

        toc: TOC = []

        for token in parser.parse(markdown):
            if token.type == "heading_open":
                block_id += 1
                stack.append(HEADINGS[token.tag](id=f"block{block_id}"))
            elif token.type == "paragraph_open":
                stack.append(Paragraph())
            elif token.type == "blockquote_open":
                stack.append(BlockQuote())
            elif token.type == "bullet_list_open":
                stack.append(BulletList())
            elif token.type == "ordered_list_open":
                stack.append(OrderedList())
            elif token.type == "list_item_open":
                stack.append(ListItem(f"{token.info}. " if token.info else "● "))
            elif token.type == "table_open":
                stack.append(Table())
            elif token.type == "tbody_open":
                stack.append(TBody())
            elif token.type == "thead_open":
                stack.append(THead())
            elif token.type == "tr_open":
                stack.append(TR())
            elif token.type == "th_open":
                stack.append(TH())
            elif token.type == "td_open":
                stack.append(TD())
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
                        elif child.type == "code_inline":
                            content.append(
                                child.content,
                                style_stack[-1]
                                + self.get_component_rich_style(
                                    "code_inline", partial=True
                                ),
                            )
                        elif child.type == "em_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("em", partial=True)
                            )
                        elif child.type == "strong_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("strong", partial=True)
                            )
                        elif child.type == "s_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("s", partial=True)
                            )
                        elif child.type == "link_open":
                            href = child.attrs.get("href", "")
                            action = f"link({href!r})"
                            style_stack.append(
                                style_stack[-1] + Style.from_meta({"@click": action})
                            )
                        elif child.type == "image":
                            href = child.attrs.get("src", "")
                            alt = child.attrs.get("alt", "")

                            action = f"link({href!r})"
                            style_stack.append(
                                style_stack[-1] + Style.from_meta({"@click": action})
                            )

                            content.append("🖼  ", style_stack[-1])
                            if alt:
                                content.append(f"({alt})", style_stack[-1])
                            for grandchild in child.children:
                                content.append(grandchild.content, style_stack[-1])

                            style_stack.pop()

                        elif child.type.endswith("_close"):
                            style_stack.pop()

                stack[-1].set_content(content)
            elif token.type == "fence":
                output.append(
                    Fence(
                        token.content.rstrip(),
                        token.info,
                    )
                )

        await self.emit(TOCUpdated(toc, sender=self))
        await self.mount(*output)


class MarkdownTOC(Widget, can_focus_children=True):
    DEFAULT_CSS = """
    MarkdownTOC {
        width: auto;
        background: $panel;
        border-right: wide $background;
    }
    MarkdownTOC > Tree {
        padding: 1;
        width: auto;
    }
    """

    toc: reactive[TOC | None] = reactive(None, init=False)

    def compose(self) -> ComposeResult:
        tree = Tree("TOC")
        tree.show_root = False
        tree.show_guides = True
        tree.guide_depth = 4
        tree.auto_expand = False
        yield tree

    def watch_toc(self, toc: TOC) -> None:
        self.set_toc(toc)

    def set_toc(self, toc: TOC) -> None:
        tree = self.query_one(Tree)
        tree.clear()
        root = tree.root
        for level, name, block_id in toc:
            node = root
            for _ in range(level - 1):
                if node._children:
                    node = node._children[-1]
                    node.expand()
                    node.allow_expand = True
                else:
                    node = node.add(NUMERALS(level), expand=True)
            node.add_leaf(f"[dim]{NUMERALS[level]}[/] {name}", {"block_id": block_id})

    async def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        await self.emit(TOCSelected(message.node.data["block_id"], sender=self))


class MarkdownBrowser(Vertical, can_focus=True, can_focus_children=True):
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

    navigator: var[Navigator] = var(Navigator)

    @property
    def document(self) -> MarkdownDocument:
        return self.query_one(MarkdownDocument)

    async def go(self, location: str) -> bool:
        return await self.document.load(self.navigator.go(location))

    async def back(self) -> None:
        if self.navigator.back():
            await self.document.load(self.navigator.location)

    async def forward(self) -> None:
        if self.navigator.forward():
            await self.document.load(self.navigator.location)

    async def on_link_clicked(self, message: LinkClicked) -> None:
        message.stop()
        await self.go(message.href)

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

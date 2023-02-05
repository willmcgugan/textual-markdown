# Textual Markdown Browser - Demo

This page contains a lot of Markdown code we will use to test the MD browser.

## Headers

Headers levels 1 through 6 are supported.

.

#### This is H4

Header level 4 content. Drilling down in to finer headings.

##### This is H5

Header level 5 content. 

###### This is H6

Header level 6 content.

## Typography

The usual Markdown typography is supported. The exact output depends on your terminal, although most are fairly consistent.

### Emphasis

Emphasis is rendered with `*asterisks*`, and looks *like this*;

### Strong

Use two asterisks to indicate strong which renders in bold, e.g. `**strong**` render **strong**.

### Strikethrough

Two tildes indicates strikethrough, e.g. `~~cross out~~` render ~~cross out~~.

### Inline code ###

Inline cod is indicated by backticks. e.g. `import this`.

## Fences

Fenced code blocks are introduced with three back-ticks and the optional parser. Here we are rendering the code in a sub-widget with syntax highlighting and indent guides.

In the future I think we could add controls to export the code, copy to the clipboard. Heck, even run it and show the output?

```python
@lru_cache(maxsize=1024)
def split(self, cut_x: int, cut_y: int) -> tuple[Region, Region, Region, Region]:
    """Split a region in to 4 from given x and y offsets (cuts).

    ```
                cut_x ↓
            ┌────────┐ ┌───┐
            │        │ │   │
            │    0   │ │ 1 │
            │        │ │   │
    cut_y → └────────┘ └───┘
            ┌────────┐ ┌───┐
            │    2   │ │ 3 │
            └────────┘ └───┘
    ```

    Args:
        cut_x (int): Offset from self.x where the cut should be made. If negative, the cut
            is taken from the right edge.
        cut_y (int): Offset from self.y where the cut should be made. If negative, the cut
            is taken from the lower edge.

    Returns:
        tuple[Region, Region, Region, Region]: Four new regions which add up to the original (self).
    """

    x, y, width, height = self
    if cut_x < 0:
        cut_x = width + cut_x
    if cut_y < 0:
        cut_y = height + cut_y

    _Region = Region
    return (
        _Region(x, y, cut_x, cut_y),
        _Region(x + cut_x, y, width - cut_x, cut_y),
        _Region(x, y + cut_y, cut_x, height - cut_y),
        _Region(x + cut_x, y + cut_y, width - cut_x, height - cut_y),
    )
```

## Quote

Quotes are introduced with a chevron, and render like this:

> I must not fear.
> Fear is the mind-killer.
> Fear is the little-death that brings total obliteration.
> I will face my fear.
> I will permit it to pass over me and through me.
> And when it has gone past, I will turn the inner eye to see its path.
> Where the fear has gone there will be nothing. Only I will remain."

Quotes nest nicely. Here's what quotes within quotes look like:

> I must not fear.
> > Fear is the mind-killer.
> > Fear is the little-death that brings total obliteration.
> > I will face my fear.
> > > I will permit it to pass over me and through me.
> > > And when it has gone past, I will turn the inner eye to see its path.
> > > Where the fear has gone there will be nothing. Only I will remain.

## Tables

Tables are supported, and render with a DataTable.

I would like to add controls to these widgets to export the table as CSV, which I think would be a nice feature. In the future we might also have sortable columns by clicking on the headers.


| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |
| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |
| `header_height` | `int`  | `1`     | Height of header row               |
| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |


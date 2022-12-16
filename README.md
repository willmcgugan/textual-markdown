# Textual Markdown Browser

Just testing various Markdown content.

[link](./demo.md)

## Typography

### Emphasis

Lets see if we can add text with *emphasis*. Typically rendered as italics.

> Lets see if we can add text with *emphasis*. Typically rendered as italics. Lets see if we can add text with *emphasis*. Typically rendered as italics.
> > Lets see if we can add text with *emphasis*. Typically rendered as italics.Lets see if we can add text with *emphasis*. Typically rendered as italics.

### Strong

We can also render **strong** text as bold.

### Strike

We can render ~~strikethrough~~ text.

## Code

Render a code "fence" with syntax highlighting.

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

## Table

Great google moogly, its a GitHub style table in a TUI!

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |
| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |
| `header_height` | `int`  | `1`     | Height of header row               |
| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |


## Bullet list

A simple list of items.

- This is a list
- Another item
  - Nested
    - List items may have *formatting*    
  - Yet another item

## Ordered List

Order lists.

1. Hello
2. World
   1. asdfsdf
   2. werwer

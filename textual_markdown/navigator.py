from __future__ import annotations

from pathlib import Path


class Navigator:
    """Manages a stack of paths like a browser."""

    def __init__(self) -> None:
        self.stack: list[Path] = []
        self.index = 0

    @property
    def location(self) -> Path:
        """The current location.

        Returns:
            Path: A path for the current document.
        """
        if not self.stack:
            return Path(".")
        return self.stack[self.index]

    def go(self, path: str) -> Path:
        """Go to a new document.

        Args:
            path (str): Path to new document.

        Returns:
            Path: New location.
        """
        new_path = self.location.parent / Path(path)
        self.stack = self.stack[: self.index + 1]
        new_path = new_path.absolute()
        self.stack.append(new_path)
        self.index = len(self.stack) - 1
        return new_path

    def back(self) -> bool:
        """Go back in the stack.

        Returns:
            bool: True if the location changed, otherwise False.
        """
        if self.index:
            self.index -= 1
            return True
        return False

    def forward(self) -> bool:
        """Go forward in the stack.

        Returns:
            bool: True if the location changed, otherwise False.
        """
        if self.index < len(self.stack) - 1:
            self.index += 1
            return True
        return False

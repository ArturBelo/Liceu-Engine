from __future__ import annotations

from .document import MarkdownDocument


class ParserPipeline:
    """Pipeline for processing MarkdownDocument instances through registered parsers."""

    def __init__(self) -> None:
        self._parsers: list[object] = []

    def register(self, parser: object) -> None:
        """Register a parser that accepts and returns a MarkdownDocument."""
        self._parsers.append(parser)

    def process(self, document: MarkdownDocument) -> MarkdownDocument:
        """Run all registered parsers sequentially."""
        current = document
        for parser in self._parsers:
            if hasattr(parser, "process"):
                current = parser.process(current)
            elif hasattr(parser, "parse"):
                current = parser.parse(current)
            else:
                raise AttributeError("Parser must implement process() or parse()")
        return current

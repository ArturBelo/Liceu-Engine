from pathlib import Path

from engine.exceptions import EngineError, ValidationError
from engine.parsers.document import MarkdownDocument
from engine.parsers.front_matter import FrontMatterParser
from engine.parsers.heading import HeadingParser
from engine.parsers.pipeline import ParserPipeline
from engine.parsers.wikilink import WikiLinkParser


class MarkdownParser:
    """Parser for Markdown files that returns a MarkdownDocument."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def parse(self) -> MarkdownDocument:
        """Parse the Markdown file and return a MarkdownDocument."""
        if not self._path.exists():
            raise EngineError(f"File not found: {self._path}")

        if self._path.suffix.lower() != ".md":
            raise ValidationError(f"Invalid markdown extension: {self._path.suffix}")

        content = self._path.read_text(encoding="utf-8")
        document = MarkdownDocument(path=self._path, content=content)

        pipeline = ParserPipeline()
        pipeline.register(FrontMatterParser())
        pipeline.register(HeadingParser())
        pipeline.register(WikiLinkParser())
        return pipeline.process(document)

import re

from .document import MarkdownDocument


class HeadingParser:
    """Extract headings from a Markdown document."""

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s*(.*)$")

    def process(self, document: MarkdownDocument) -> MarkdownDocument:
        """Collect all Markdown headings without modifying content."""
        headings: list[str] = []
        for line in document.content.splitlines():
            stripped = line.lstrip()
            match = self.HEADING_PATTERN.match(stripped)
            if match:
                heading_text = match.group(2).strip()
                headings.append(heading_text)

        return MarkdownDocument(
            path=document.path,
            content=document.content,
            front_matter=document.front_matter,
            headings=headings,
            tags=document.tags,
            wikilinks=document.wikilinks,
            images=document.images,
            tables=document.tables,
            code_blocks=document.code_blocks,
        )

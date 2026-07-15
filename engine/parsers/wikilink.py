import re

from .document import MarkdownDocument


class WikiLinkParser:
    """Extract Obsidian-style wiki links from a Markdown document."""

    WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

    def process(self, document: MarkdownDocument) -> MarkdownDocument:
        """Collect wiki links and preserve document content."""
        wikilinks: list[str] = []
        for match in self.WIKILINK_PATTERN.finditer(document.content):
            wikilinks.append(match.group(1).strip())

        return MarkdownDocument(
            path=document.path,
            content=document.content,
            front_matter=document.front_matter,
            headings=document.headings,
            tags=document.tags,
            wikilinks=wikilinks,
            images=document.images,
            tables=document.tables,
            code_blocks=document.code_blocks,
        )

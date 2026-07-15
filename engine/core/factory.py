from engine.parsers.document import MarkdownDocument

from .knowledge import Knowledge


class KnowledgeFactory:
    """Build Knowledge domain objects from Markdown documents."""

    @staticmethod
    def from_markdown(document: MarkdownDocument) -> Knowledge:
        """Create a Knowledge instance from a MarkdownDocument."""
        title = ""
        metadata = document.front_matter or {}

        if isinstance(metadata.get("title"), str) and metadata.get("title"):
            title = metadata["title"]
        elif document.headings:
            title = document.headings[0]
        else:
            title = document.path.stem

        return Knowledge(
            title=title,
            content=document.content,
            tags=list(document.tags),
            headings=list(document.headings),
            wikilinks=list(document.wikilinks),
            metadata=dict(metadata),
        )

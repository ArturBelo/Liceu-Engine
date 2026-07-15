from pathlib import Path

from engine.core import KnowledgeFactory, KnowledgeRepository, KnowledgeService
from engine.parsers import MarkdownParser


class LiceuEngine:
    """Facade for the Liceu Engine public API."""

    def __init__(self) -> None:
        self._repository = KnowledgeRepository()
        self._service = KnowledgeService(self._repository)

    def add_markdown(self, path: Path):
        """Parse a Markdown file and add it to the knowledge repository."""
        document = MarkdownParser(path).parse()
        knowledge = KnowledgeFactory.from_markdown(document)
        return self._service.create(
            title=knowledge.title,
            content=knowledge.content,
            tags=knowledge.tags,
            headings=knowledge.headings,
            wikilinks=knowledge.wikilinks,
            metadata=knowledge.metadata,
        )

    def import_directory(self, path: Path):
        """Import all Markdown files from a directory recursively."""
        directory = Path(path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        if not directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")

        markdown_files = sorted(
            [file for file in directory.rglob("*") if file.is_file() and file.suffix.lower() == ".md"],
            key=lambda file: str(file),
        )

        imported = []
        for markdown_file in markdown_files:
            imported.append(self.add_markdown(markdown_file))

        return imported

    def list(self, limit: int | None = None, offset: int = 0, order_by: str = "created_at", descending: bool = False):
        """List knowledge items from the repository."""
        return self._service.list(limit=limit, offset=offset, order_by=order_by, descending=descending)

    def search(self, query: str):
        """Search knowledge items by query text."""
        return self._service.search(query)

    def count(self) -> int:
        """Return the number of knowledge items stored."""
        return len(self._service.list())

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MarkdownDocument:
    """Represents a Markdown document loaded by the parser."""

    path: Path
    content: str
    front_matter: dict[str, object] | None = None
    headings: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    tables: list[str] = field(default_factory=list)
    code_blocks: list[str] = field(default_factory=list)

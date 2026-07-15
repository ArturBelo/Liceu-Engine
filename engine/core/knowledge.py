from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Knowledge:
    """Represents a knowledge item stored by the engine."""

    id: UUID = field(default_factory=uuid4)
    title: str = ""
    content: str = ""
    tags: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    wikilinks: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

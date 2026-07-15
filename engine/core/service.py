from dataclasses import replace
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from .interfaces import IKnowledgeRepository
from .knowledge import Knowledge


class KnowledgeService:
    """Service layer for Knowledge entity operations."""

    def __init__(self, repository: IKnowledgeRepository) -> None:
        self._repository = repository

    def create(
        self,
        title: str,
        content: str,
        tags: list[str] | None = None,
        headings: list[str] | None = None,
        wikilinks: list[str] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> Knowledge:
        """Create a new Knowledge item and add it to the repository."""
        knowledge = Knowledge(
            title=title,
            content=content,
            tags=tags or [],
            headings=headings or [],
            wikilinks=wikilinks or [],
            metadata=metadata or {},
        )
        self._repository.add(knowledge)
        return knowledge

    def get(self, id: UUID) -> Optional[Knowledge]:
        """Return a Knowledge item by ID, or None if not found."""
        return self._repository.get(id)

    def list(
        self,
        limit: int | None = None,
        offset: int = 0,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> List[Knowledge]:
        """Return a sorted and paginated list of Knowledge items."""
        return self._repository.list(limit=limit, offset=offset, order_by=order_by, descending=descending)

    def delete(self, id: UUID) -> bool:
        """Remove a Knowledge item by ID."""
        return self._repository.remove(id)

    def search(self, query: str) -> List[Knowledge]:
        """Search knowledge items by query text."""
        return self._repository.search(query)

    def update(
        self, id: UUID, title: str, content: str, tags: list[str]
    ) -> Optional[Knowledge]:
        """Update an existing Knowledge item and return the updated entity."""
        existing = self._repository.get(id)
        if existing is None:
            return None

        updated_knowledge = replace(
            existing,
            title=title,
            content=content,
            tags=tags,
            updated_at=datetime.now(timezone.utc),
        )
        self._repository.update(updated_knowledge)
        return updated_knowledge

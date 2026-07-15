from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from .interfaces import IKnowledgeRepository
from .knowledge import Knowledge


class KnowledgeRepository(IKnowledgeRepository):
    """In-memory repository for Knowledge entities."""

    def __init__(self) -> None:
        self._items: List[Knowledge] = []

    def add(self, knowledge: Knowledge) -> None:
        """Add a Knowledge item to the repository."""
        self._items.append(knowledge)

    def get(self, id: UUID) -> Optional[Knowledge]:
        """Return a Knowledge item by ID, or None if not found."""
        for item in self._items:
            if item.id == id:
                return item
        return None

    def list(
        self,
        limit: int | None = None,
        offset: int = 0,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> List[Knowledge]:
        """Return a sorted and paginated copy of stored Knowledge items."""
        valid_order_fields = {"created_at", "updated_at", "title"}
        if order_by not in valid_order_fields:
            order_by = "created_at"

        items = sorted(
            self._items,
            key=lambda item: getattr(item, order_by),
            reverse=descending,
        )
        start = max(offset, 0)
        end = None if limit is None else start + limit
        return items[start:end]

    def remove(self, id: UUID) -> bool:
        """Remove the Knowledge item with the given ID."""
        for index, item in enumerate(self._items):
            if item.id == id:
                del self._items[index]
                return True
        return False

    def update(self, knowledge: Knowledge) -> bool:
        """Update an existing Knowledge item with the same ID."""
        for index, item in enumerate(self._items):
            if item.id == knowledge.id:
                self._items[index] = knowledge
                return True
        return False

    def search(self, query: str) -> list[Knowledge]:
        """Search knowledge items by title or content, case insensitive."""
        query_lower = query.lower()
        return [
            item
            for item in self._items
            if query_lower in item.title.lower() or query_lower in item.content.lower()
        ]

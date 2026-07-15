from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from .knowledge import Knowledge


class KnowledgeRepository:
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

    def list(self) -> List[Knowledge]:
        """Return a copy of all stored Knowledge items."""
        return list(self._items)

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

from dataclasses import replace
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from .knowledge import Knowledge
from .repository import KnowledgeRepository


class KnowledgeService:
    """Service layer for Knowledge entity operations."""

    def __init__(self, repository: KnowledgeRepository) -> None:
        self._repository = repository

    def create(self, title: str, content: str, tags: list[str] | None = None) -> Knowledge:
        """Create a new Knowledge item and add it to the repository."""
        knowledge = Knowledge(title=title, content=content, tags=tags or [])
        self._repository.add(knowledge)
        return knowledge

    def get(self, id: UUID) -> Optional[Knowledge]:
        """Return a Knowledge item by ID, or None if not found."""
        return self._repository.get(id)

    def list(self) -> List[Knowledge]:
        """Return all Knowledge items from the repository."""
        return self._repository.list()

    def delete(self, id: UUID) -> bool:
        """Remove a Knowledge item by ID."""
        return self._repository.remove(id)

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

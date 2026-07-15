from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from .knowledge import Knowledge


class IKnowledgeRepository(ABC):
    """Abstract repository interface for Knowledge entities."""

    @abstractmethod
    def add(self, knowledge: Knowledge) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: UUID) -> Optional[Knowledge]:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        limit: int | None = None,
        offset: int = 0,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> list[Knowledge]:
        """Return a page of knowledge items.

        limit None returns all items.
        offset defines the start of the read.
        order_by accepts only created_at, updated_at or title.
        Invalid values default to created_at.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, knowledge: Knowledge) -> bool:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> list[Knowledge]:
        """Search for knowledge items by query text."""
        raise NotImplementedError

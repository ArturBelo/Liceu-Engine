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
    def list(self) -> list[Knowledge]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, knowledge: Knowledge) -> bool:
        raise NotImplementedError

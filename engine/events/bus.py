from __future__ import annotations

from collections import defaultdict
from typing import Callable, Dict, List, Type

from .events import Event


class EventBus:
    """Simple event bus for publishing and subscribing to events."""

    def __init__(self) -> None:
        self._listeners: Dict[Type[Event], List[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], callback: Callable[[Event], None]) -> None:
        """Register a callback for the given event type."""
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: Type[Event], callback: Callable[[Event], None]) -> None:
        """Remove a previously registered callback for the event type."""
        listeners = self._listeners.get(event_type)
        if listeners is None:
            return
        try:
            listeners.remove(callback)
        except ValueError:
            pass

    def publish(self, event: Event) -> None:
        """Publish an event to all registered listeners for its type."""
        for callback in list(self._listeners.get(type(event), [])):
            callback(event)
